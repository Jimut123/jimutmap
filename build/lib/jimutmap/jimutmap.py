"""
This program downloads / scrapes Apple maps for free.
OPEN SOURCED UNDER GPL-V3.0.
Author : Jimut Bahan Pal | jimutbahanpal@yahoo.com
"""
#pylint: disable= global-statement
#cSpell:words imghdr, tqdm, asinh, jimut, bahan
# imports

import ssl
import os
import time
import math
from os.path import join, exists, normpath, relpath
import imghdr
from multiprocessing.pool import ThreadPool
from typing import Tuple
from tqdm import tqdm
import numpy as np
import requests
from selenium import webdriver
import chromedriver_autoinstaller

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'
}

# To synchronize

LOCK_VAR = 0
UNLOCK_VAR = 0
LOCKING_LIMIT = 50 # MAX NO OF THREADS


class api:
    """
    Pull tiles from Apple Maps
    """
    def __init__(self, min_lat_deg:float, max_lat_deg:float, min_lon_deg:float, max_lon_deg:float, zoom= 19, ac_key:str= None, verbose:bool= False, threads_:int= 4, container_dir:str= ""):
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
            Thread limit for process. Max 50

        container_dir:str (default= "")
            When downloading images, place them in this directory.
            It will be created if it does not exist.
        """
        global LOCKING_LIMIT
        self._acKey = None
        self._containerDir = ""
        if ac_key is None:
            self._getAPIKey()
        else:
            self.ac_key = ac_key
        self.set_bounds(min_lat_deg, max_lat_deg, min_lon_deg, max_lon_deg)
        self.zoom = zoom
        self.verbose = bool(verbose)
        LOCKING_LIMIT = threads_
        if self.verbose:
            print(self.ac_key,self.min_lat_deg,self.max_lat_deg,self.min_lon_deg,self.max_lon_deg,self.zoom,self.verbose,LOCKING_LIMIT)
        self._getMasks = True
        self.container_dir = container_dir

    @property
    def container_dir(self) -> str:
        """
        Get the output directory
        """
        return self._containerDir

    @container_dir.setter
    def container_dir(self, newDir:str):
        try:
            if isinstance(newDir, str) and len(newDir) > 0:
                newDir = normpath(relpath(newDir))
                if not exists(newDir):
                    if self.verbose:
                        print(f"Creating target directory `{newDir}`")
                    os.makedirs(newDir)
                assert exists(newDir)
                self._containerDir = newDir
        except Exception: #pylint: disable= broad-except
            self._containerDir = ""


    def set_bounds(self, min_lat_deg:float, max_lat_deg:float, min_lon_deg:float, max_lon_deg:float):
        """
        Set the viewport bounds
        """
        assert -90 < min_lat_deg < 90
        assert -90 < max_lat_deg < 90
        assert min_lat_deg < max_lat_deg
        assert -180 < min_lon_deg < 180
        assert -180 < max_lon_deg < 180
        assert min_lon_deg < max_lon_deg
        # For compatibility with other funcs,
        # explicitly cast to float
        self.min_lat_deg = float(min_lat_deg)
        self.max_lat_deg = float(max_lat_deg)
        self.min_lon_deg = float(min_lon_deg)
        self.max_lon_deg = float(max_lon_deg)

    def _getLatBounds(self) -> Tuple[float, float]:
        """
        Internal getter for (min, max) latitude
        """
        return self.min_lat_deg, self.max_lat_deg

    def _getLonBounds(self) -> Tuple[float, float]:
        """
        Internal getter for (min, max) longitude
        """
        return self.min_lon_deg, self.max_lon_deg

    @property
    def ac_key(self) -> str:
        """
        Get or set the internal accessKey for the tile requests
        """
        return self._acKey

    @ac_key.setter
    def ac_key(self, newACKey:str):
        try:
            if not newACKey.startswith("&"):
                if not newACKey.lower().startswith("a"):
                    newACKey = f"accessKey={newACKey}"
                newACKey = f"&{newACKey}"
            self._acKey = newACKey
        except (AttributeError, TypeError):
            self._acKey = None
            if newACKey is not None:
                raise ValueError("Invalid AccessKey string")

    def _getAPIKey(self) -> str:
        """
        Use a headless Chrome/Chromium instance to scrape the access key
        from the data-map-printing-background attribute of Apple Maps.
        """
        SAMPLE_KEY = r"1614125879_3642792122889215637_%2F_RwvhYZM5fKknqTdkXih2Wcu3s2f3Xea126uoIuDzUIY%3D"
        KEY_START = r"&accessKey="
        chromeDriverPath = chromedriver_autoinstaller.install(cwd= True)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(executable_path= chromeDriverPath, options=options)
        driver.get("https://satellites.pro/USA_map#37.405074,-94.284668,5")
        time.sleep(5)
        baseMap = driver.find_element_by_css_selector("#map-canvas .leaflet-mapkit-mutant")
        mapData = baseMap.get_attribute("data-map-printing-background")
        accessKeyStart = mapData.find(KEY_START)
        accessKeyEnd = accessKeyStart + int(1.5 * len(SAMPLE_KEY))
        searchForKey = mapData[accessKeyStart:accessKeyEnd]
        keyContents = searchForKey[len(KEY_START):]
        keyEnd = keyContents.find("&")
        keyContents = keyContents[:keyEnd]
        self.ac_key = keyContents
        return keyContents


    def ret_xy_tiles(self, lat_deg:float, lon_deg:float) -> Tuple[int, int]:
        """
        Parameters
        -----------------------

        lat_deg:float
        lon_deg:float

        Returns
        ----------------------
        tuple: (xTile, yTile)
        """
        n = 2**self.zoom
        xTile = n * ((lon_deg + 180) / 360)
        lat_rad = lat_deg * math.pi / 180.0
        yTile = n * (1 - (math.log(math.tan(lat_rad) + 1/math.cos(lat_rad)) / math.pi)) / 2
        return int(xTile),int(yTile)

    def ret_lat_lon(self, xTile:int, yTile:int) -> Tuple[float, float]:
        """
        Parameters
        -----------------------

        xTile:int
        yTile:int

        Returns
        ----------------------
        tuple: (lat, lng)
        """
        n = 2**self.zoom
        lon_deg = int(xTile)/n * 360.0 - 180.0
        lat_rad = math.atan(math.asinh(math.pi * (1 - 2 * int(yTile)/n)))
        lat_deg = lat_rad * 180.0 / math.pi
        return lat_deg, lon_deg

    def make_url(self, lat_deg:float, lon_deg:float):
        """
        returns the list of urls when lat, lon, zoom and accessKey is provided

        Parameters
        -----------------------

        lat_deg:float
        lon_deg:float
        """
        xTile, yTile = self.ret_xy_tiles(lat_deg, lon_deg)
        return [xTile, yTile]

    def get_img(self, url_str:str, vNumber:int= 9042, getMask:bool= None, prefix:str= "", _rerun:bool= False):
        """
        Get images from the URL provided and save them

        Parameters
        --------------------
        url_str:str
            The URL to read

        vNumber:int (default= 9042)
            The original version of this number was hardcoded as 7072,
            which was no longer working. Moved to a kwarg.

        getMask:bool (default= None)
            By default, uses the internal self._getMasks variable set
            on instantiation. If set to a boolean value, overrides the
            current self._getMasks value

        _rerun:bool (default= False)
            Internal. Tracks retry status.
        """
        global headers, LOCK_VAR, UNLOCK_VAR, LOCKING_LIMIT
        if isinstance(getMask, bool):
            self._getMasks = getMask
        getMask = self._getMasks
        if self.verbose:
            print(url_str)
        UNLOCK_VAR = UNLOCK_VAR + 1
        LOCK_VAR = 1
        if self.verbose:
            print("UNLOCK VAR : ",UNLOCK_VAR)
        if UNLOCK_VAR >= LOCKING_LIMIT:
            LOCK_VAR = 0
            UNLOCK_VAR = 0
            if self.verbose:
                print("-------- UNLOCKING")
        xTile = url_str[0]
        yTile = url_str[1]
        file_name = join(self.container_dir, f"{prefix}{xTile}_{yTile}.jpg")
        try:
            assert exists(file_name)
        except AssertionError:
            try:
                # get the image tile and the mask tile for the same
                req_url = f"https://sat-cdn1.apple-mapkit.com/tile?style=7&size=1&scale=1&z={self.zoom}&x={xTile}&y={yTile}&v={vNumber}{self.ac_key}"
                if self.verbose:
                    print(req_url)
                r = requests.get(req_url, headers= headers)
                try:
                    if "access denied" in str(r.content).lower():
                        if _rerun:
                            return False
                        # Refresh the API key
                        self._getAPIKey()
                        return self.get_img(url_str, vNumber, getMask, _rerun= True)
                except Exception: #pylint: disable= broad-except
                    pass
                with open(file_name, 'wb') as fh:
                    fh.write(r.content)
                if imghdr.what(file_name) is 'jpeg':
                    if self.verbose:
                        print(file_name,"JPEG")
                else:
                    os.remove(file_name)
                    if self.verbose:
                        print(file_name, "NOT JPEG")
            except Exception as e: #pylint: disable= broad-except
                if self.verbose:
                    print(e)
        if getMask:
            ext = file_name.split('.').pop()
            file_name_road = file_name[:-len(ext)]+"_road.png"
            try:
                assert exists(file_name_road)
            except AssertionError:
                for cdnLevel in range(1, 5):
                    req_url = f"https://cdn{cdnLevel}.apple-mapkit.com/ti/tile?country=US&region=US&style=46&size=1&x={xTile}&y={yTile}&z={self.zoom}&scale=1&lang=en&v=2008184&poi=0{self.ac_key}&labels=0"
                    try:
                        # image and mask retrieval
                        # For the roads data
                        if self.verbose:
                            print(req_url)
                        r = requests.get(req_url, headers= headers)
                        with open(file_name_road, 'wb') as fh:
                            fh.write(r.content)
                        if imghdr.what(file_name_road) is 'png':
                            if self.verbose:
                                print(file_name_road,"PNG")
                            break # Success
                        else:
                            os.remove(file_name_road)
                            if self.verbose:
                                print(file_name_road,"NOT PNG")
                    except Exception as e: #pylint: disable= broad-except
                        if self.verbose:
                            print(e)

    def download(self, getMasks:bool= False, latLonResolution:float= 0.0005, **kwargs):
        """
        Downloads the tiles as initialized.

        Parameters
        --------------------------------

        getMasks:bool (default= False)
            Download the road PNG mask tile if true

        latLonResolution:float (default= 0.0005)
            The step size to use when creating tiles

        Also accepts kwargs for `get_img`.
        """
        self._getMasks = bool(getMasks)
        min_lat, max_lat = self._getLatBounds()
        min_lon, max_lon = self._getLonBounds()
        if (max_lat - min_lat <= latLonResolution) or (max_lon - min_lon <= latLonResolution):
            # If we fail this check, then our arange will return no
            # results and we'll fetch nothing
            raise ValueError(f"Latitude and longitude bounds must be separated by at least the latLonResolution (currently {latLonResolution}). Either shrink the resolution value or increase the separation of your minimum/maximum latitude and longitude.")

        for i in tqdm(np.arange(min_lat, max_lat, latLonResolution)):
            tp = None
            URL_ALL = []
            for j in np.arange(min_lon, max_lon, latLonResolution):
                URL_ALL.append(self.make_url(i,j))
            if self.verbose:
                print("ALL URL CREATED! ...")
            global LOCK_VAR, UNLOCK_VAR, LOCKING_LIMIT
            if LOCK_VAR == 0:
                if self.verbose:
                    print("LOCKING")
                LOCK_VAR = 1
                UNLOCK_VAR = 0
                tp = ThreadPool(LOCKING_LIMIT)
                tp.imap_unordered(lambda x: self.get_img(x, **kwargs), URL_ALL) #pylint: disable= unnecessary-lambda #cSpell:words imap
                tp.close()
            # SEMAPHORE KINDA THINGIE
            if UNLOCK_VAR >= LOCKING_LIMIT and tp is not None:
                # If we have too many threads running, explicitly call
                # a wait on the threads until the most recent
                # process has cleared. As a practical matter, this will
                # clear _several_ threads and keep up performance
                tp.join()
