# ========================================================
# This program fetches tiles from satellites.pro for free.
# OPEN SOURCED UNDER GPL-V3.0.
# Author : Jimut Bahan Pal | jimutbahanpal@yahoo.com
# Project Website: https://github.com/Jimut123/jimutmap
# pylint: disable = global-statement
# cSpell: words imghdr, tqdm, asinh, jimut, bahan
# ========================================================

import ssl
import os
import re
import time
import math
import urllib.parse
import requests
import numpy as np
import datetime as dt
from tqdm import tqdm
import multiprocessing
from typing import Tuple
from os.path import join, exists, normpath, relpath
from multiprocessing.pool import ThreadPool

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

try:
    import undetected_chromedriver as uc
except ImportError:
    print("Install: pip install undetected-chromedriver")
    exit()

try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    print("Install: pip install Pillow")
    exit()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

class api:
    def __init__(self, min_lat_deg:float, max_lat_deg:float, min_lon_deg:float, max_lon_deg:float, zoom=19, ac_key:str=None, verbose:bool=False, threads_:int=4, container_dir:str=""):
        """
        Parameters
        -------------------------------------

        min_lat_deg: float
        max_lat_deg: float
        min_lon_deg: float
        max_lon_deg: float

        zoom: int
            Zoom level. Between  1 and 20.

        ac_key:str (default= None)
            Access key to Apple Maps. If not provided, will use a headless Chrome instance to fetch a session key.

        verbose:bool (default= False)
            Helpful debugging output

        threads_: int (default= 4)
            Thread limit for process. Max depending on CPU cores

        container_dir:str (default= "")
            When downloading images, place them in this directory.
            It will be created if it does not exist.
        """
        self._acKey = None
        self._containerDir = ""
        self.verbose = bool(verbose)
        
        if ac_key is None:
            self._getAPIKey()
        else:
            self.ac_key = ac_key
            
        self.set_bounds(min_lat_deg, max_lat_deg, min_lon_deg, max_lon_deg)
        self.zoom = zoom
        self.threads = min(threads_, multiprocessing.cpu_count())
        self._getMasks = True
        self.container_dir = container_dir

    @property
    def container_dir(self):
        return self._containerDir

    @container_dir.setter
    def container_dir(self, newDir):
        try:
            if isinstance(newDir, str) and len(newDir) > 0:
                newDir = normpath(relpath(newDir))
                if not exists(newDir):
                    os.makedirs(newDir)
                self._containerDir = newDir
        except Exception:
            self._containerDir = ""

    def set_bounds(self, min_lat_deg, max_lat_deg, min_lon_deg, max_lon_deg):
        assert -90 < min_lat_deg < 90 and -90 < max_lat_deg < 90
        assert min_lat_deg < max_lat_deg
        assert -180 < min_lon_deg < 180 and -180 < max_lon_deg < 180
        assert min_lon_deg < max_lon_deg
        self.min_lat_deg = float(min_lat_deg)
        self.max_lat_deg = float(max_lat_deg)
        self.min_lon_deg = float(min_lon_deg)
        self.max_lon_deg = float(max_lon_deg)

    def _getLatBounds(self):
        return self.min_lat_deg, self.max_lat_deg

    def _getLonBounds(self):
        return self.min_lon_deg, self.max_lon_deg

    @property
    def ac_key(self):
        return self._acKey

    @ac_key.setter
    def ac_key(self, newACKey):
        try:
            if 'accessKey=' in newACKey:
                newACKey = newACKey.split('accessKey=')[1]
            self._acKey = f"&accessKey={newACKey}"
        except (AttributeError, TypeError):
            self._acKey = None
            if newACKey is not None:
                raise ValueError("Invalid AccessKey string")

    def _create_fresh_options(self):
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--allow-running-insecure-content")
        
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,
                "media_stream": 2,
            }
        }
        options.add_experimental_option("prefs", prefs)
        return options

    def _getAPIKey(self, timeout: float = 60):
        driver = None
        
        initialization_methods = [
            lambda: uc.Chrome(options=self._create_fresh_options()),
            lambda: uc.Chrome(options=self._create_fresh_options(), use_subprocess=True),
            lambda: uc.Chrome(options=self._create_fresh_options(), version_main=133),
            lambda: uc.Chrome(options=self._create_fresh_options(), version_main=132),
            lambda: uc.Chrome(options=self._create_fresh_options(), version_main=134),
            lambda: uc.Chrome(options=self._create_fresh_options(), driver_executable_path=None),
        ]
        
        for i, method in enumerate(initialization_methods):
            try:
                driver = method()
                break
            except Exception as e:
                continue
        
        if driver is None:
            raise Exception("Could not initialize Chrome")
        
        try:
            driver.get("https://satellites.pro/USA_map#37.405074,-94.284668,5")
            time.sleep(8)
            
            driver.execute_script("""
                window.capturedRequests = [];
                window.accessKeyExtracted = false;
                
                function captureURL(url) {
                    if (url && typeof url === 'string' && 
                        (url.includes('sat-cdn1.apple-mapkit.com/tile') || 
                         url.includes('sat-cdn2.apple-mapkit.com/tile') || 
                         url.includes('sat-cdn3.apple-mapkit.com/tile') || 
                         url.includes('sat-cdn4.apple-mapkit.com/tile')) && 
                        url.includes('accessKey=') &&
                        !window.capturedRequests.includes(url)) {
                        window.capturedRequests.push(url);
                        return true;
                    }
                    return false;
                }
                
                const originalFetch = window.fetch;
                window.fetch = function(...args) {
                    captureURL(args[0]);
                    return originalFetch.apply(this, args);
                };
                
                const originalXHROpen = XMLHttpRequest.prototype.open;
                XMLHttpRequest.prototype.open = function(method, url) {
                    captureURL(url);
                    return originalXHROpen.apply(this, arguments);
                };
                
                const observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        mutation.addedNodes.forEach(function(node) {
                            if (node.tagName === 'IMG' && node.src) {
                                captureURL(node.src);
                            }
                        });
                    });
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
            """)
            
            strategies = [
                self._zoom_strategy,
                self._pan_strategy,
                self._click_strategy,
                self._scroll_strategy
            ]
            
            for strategy in strategies:
                try:
                    key = strategy(driver)
                    if key:
                        return key
                except:
                    continue
            
            captured_requests = driver.execute_script("return window.capturedRequests;")
            for url in captured_requests:
                key = self._extract_access_key(url)
                if key:
                    return key
            
            raise ValueError("Could not extract API key")
            
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def _extract_access_key(self, url):
        if 'accessKey=' in url and ('sat-cdn' in url and 'apple-mapkit.com/tile' in url):
            match = re.search(r'accessKey=([^&\s]+)', url)
            if match:
                key = urllib.parse.unquote(match.group(1))
                if len(key) > 10:
                    self.ac_key = key
                    return key
        return None

    def _zoom_strategy(self, driver):
        try:
            zoom_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.leaflet-control-zoom-in"))
            )
            for _ in range(7):
                zoom_button.click()
                time.sleep(2)
                
                captured_requests = driver.execute_script("return window.capturedRequests;")
                for url in captured_requests:
                    key = self._extract_access_key(url)
                    if key:
                        return key
        except:
            pass
        return None

    def _pan_strategy(self, driver):
        try:
            actions = [
                "window.scrollBy(-400, 0)",
                "window.scrollBy(800, 0)",
                "window.scrollBy(-400, -400)",
                "window.scrollBy(0, 800)",
            ]
            
            for action in actions:
                driver.execute_script(action)
                time.sleep(2)
                
                captured_requests = driver.execute_script("return window.capturedRequests;")
                for url in captured_requests:
                    key = self._extract_access_key(url)
                    if key:
                        return key
        except:
            pass
        return None

    def _click_strategy(self, driver):
        try:
            driver.execute_script("""
                const mapElement = document.querySelector('#map, .leaflet-container, .map-container') || document.body;
                const rect = mapElement.getBoundingClientRect();
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;
                
                const positions = [
                    [centerX, centerY],
                    [centerX - 150, centerY - 150],
                    [centerX + 150, centerY + 150],
                    [centerX - 200, centerY],
                    [centerX + 200, centerY]
                ];
                
                positions.forEach((pos, index) => {
                    setTimeout(() => {
                        const event = new MouseEvent('click', {
                            view: window,
                            bubbles: true,
                            cancelable: true,
                            clientX: pos[0],
                            clientY: pos[1]
                        });
                        mapElement.dispatchEvent(event);
                    }, index * 600);
                });
            """)
            
            time.sleep(4)
            
            captured_requests = driver.execute_script("return window.capturedRequests;")
            for url in captured_requests:
                key = self._extract_access_key(url)
                if key:
                    return key
        except:
            pass
        return None

    def _scroll_strategy(self, driver):
        try:
            driver.execute_script("""
                const mapElement = document.querySelector('#map, .leaflet-container, .map-container') || document.body;
                
                for (let i = 0; i < 6; i++) {
                    setTimeout(() => {
                        const wheelEvent = new WheelEvent('wheel', {
                            view: window,
                            bubbles: true,
                            cancelable: true,
                            deltaY: i % 2 === 0 ? -120 : 120
                        });
                        mapElement.dispatchEvent(wheelEvent);
                    }, i * 1200);
                }
            """)
            
            time.sleep(8)
            
            captured_requests = driver.execute_script("return window.capturedRequests;")
            for url in captured_requests:
                key = self._extract_access_key(url)
                if key:
                    return key
        except:
            pass
        return None

    def ret_xy_tiles(self, lat_deg, lon_deg):
        n = 2**self.zoom
        xTile = n * ((lon_deg + 180) / 360)
        lat_rad = math.radians(lat_deg)
        yTile = n * (1 - (math.log(math.tan(lat_rad) + 1/math.cos(lat_rad)) / math.pi)) / 2
        return int(xTile), int(yTile)

    def get_img(self, tile_coords: Tuple[int, int], vNumber:int=10221, getMask:bool=None, prefix:str="", _rerun:bool=False):
        if isinstance(getMask, bool):
            self._getMasks = getMask
        
        xTile, yTile = tile_coords
        file_name = join(self.container_dir, f"{prefix}{xTile}_{yTile}.jpg")
        
        if exists(file_name):
            return

        try:
            req_url = f"https://sat-cdn1.apple-mapkit.com/tile?style=7&size=1&scale=1&z={self.zoom}&x={xTile}&y={yTile}&v={vNumber}{self.ac_key}"
            r = requests.get(req_url, headers=headers)
            r.raise_for_status()

            if "access denied" in str(r.content).lower():
                if _rerun:
                    return
                self._getAPIKey()
                self.get_img(tile_coords, vNumber, getMask, prefix, _rerun=True)
                return

            with open(file_name, 'wb') as fh:
                fh.write(r.content)
            
            try:
                with Image.open(file_name) as img:
                    if img.format != 'JPEG':
                        os.remove(file_name)
            except (UnidentifiedImageError, ValueError):
                if exists(file_name):
                    os.remove(file_name)

        except:
            pass

        if self._getMasks:
            file_name_road = join(self.container_dir, f"{prefix}{xTile}_{yTile}_road.png")
            if exists(file_name_road):
                return

            env_key = dt.date.today().strftime('%Y%m%d')
            for cdenLevel in range(1, 5):
                try:
                    req_url_road = f"https://cdn{cdenLevel}.apple-mapkit.com/ti/tile?country=US&style=46&size=1&x={xTile}&y={yTile}&z={self.zoom}&scale=1&v={env_key}4&poi=1{self.ac_key}"
                    r_road = requests.get(req_url_road, headers=headers)
                    r_road.raise_for_status()

                    with open(file_name_road, 'wb') as fh:
                        fh.write(r_road.content)
                    
                    try:
                        with Image.open(file_name_road) as img:
                            if img.format == 'PNG':
                                break
                        os.remove(file_name_road)
                    except:
                        if exists(file_name_road):
                            os.remove(file_name_road)
                except:
                    continue

    def download(self, getMasks:bool=False, latLonResolution:float=0.0005, **kwargs):
        self._getMasks = bool(getMasks)
        min_lat, max_lat = self._getLatBounds()
        min_lon, max_lon = self._getLonBounds()
        
        lat_steps = np.arange(min_lat, max_lat, latLonResolution)
        lon_steps = np.arange(min_lon, max_lon, latLonResolution)
        
        unique_tiles = set()
        for i in lat_steps:
            for j in lon_steps:
                unique_tiles.add(self.ret_xy_tiles(i, j))
        
        tile_list = list(unique_tiles)
        
        with ThreadPool(self.threads) as pool:
            pbar = tqdm(total=len(tile_list), desc="Downloading Tiles")
            for _ in pool.imap_unordered(lambda coords: self.get_img(coords, getMask=getMasks, **kwargs), tile_list):
                pbar.update(1)
            pbar.close()

if __name__ == '__main__':
    min_latitude = 40.781
    max_latitude = 40.783
    min_longitude = -73.967
    max_longitude = -73.964
    
    mapper = api(
        min_lat_deg=min_latitude,
        max_lat_deg=max_latitude,
        min_lon_deg=min_longitude,
        max_lon_deg=max_longitude,
        zoom=19,
        threads_=8,
        container_dir="map_tiles"
    )
    
    mapper.download(getMasks=True)
