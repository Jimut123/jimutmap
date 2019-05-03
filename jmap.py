import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import os
import wget
import imghdr
import shutil
import numpy as np
import requests
from time import time as timer
from multiprocessing.pool import ThreadPool
import time
import math
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'#,
    #'From': 'youremail@domain.com'  # This is another valid field
}

LOCK_VAR = 0
UNLOCK_VAR = 0
LOCKING_LIMIT = 50 # MAX NO OF THREADS
# https://sat-cdn2.apple-mapkit.com/tile?style=7&size=1&scale=1&z=19&x=289808&y=238513&v=4072&accessKey=1556903270_5215579321017512928_%2F_q0%2B6IlMhz2PBhhaYAP3dfwNP4ljXIXe2fJtTNx5pC5Y%3D&emphasis=standard&tint=dark
# https://sat-cdn3.apple-mapkit.com/tile?style=7&size=1&scale=1&z=19&x=97496&y=201038&v=4072&accessKey=1556903619_2786168994573642268_%2F_J3koxLSTvwJHwL0tHgR5SkpU6C5VBpbNh1wY0%2FSPWBk%3D&emphasis=standard&tint=dark

class api:
    def __init__(self,ac_key,min_lat_deg,max_lat_deg,min_lon_deg,max_lon_deg,zoom=19):

        self.ac_key = ac_key
        self.min_lat_deg = min_lat_deg
        self.max_lat_deg = max_lat_deg
        self.min_lon_deg = min_lon_deg
        self.max_lon_deg = max_lon_deg
        self.zoom = zoom

    def ret_xy_tiles(self,lat_deg,lon_deg):
        # changes for 0.0005
        # This function returns the tilex and tiley in tuple
        # Takes latitude, longitude and zoom_level
        n = 2**self.zoom
        xtile = n * ((lon_deg + 180) / 360)
        lat_rad = lat_deg * math.pi / 180.0
        ytile = n * (1 - (math.log(math.tan(lat_rad) + 1/math.cos(lat_rad)) / math.pi)) / 2
        return int(xtile),int(ytile)

    def ret_lat_lon(self,x_tyle,y_tyle):
        # This function returns the lat, lon as a tuple
        # Takes x_tyle, y_tyle and zoom_level
        n = 2**self.zoom
        lon_deg = int(x_tyle)/n * 360.0 - 180.0
        lat_rad = math.atan(math.asinh(math.pi * (1 - 2 * int(y_tyle)/n)))
        lat_deg = lat_rad * 180.0 / math.pi
        return lat_deg, lon_deg
    
    def make_url(self,lat_deg,lon_deg):
        # returns the list of urls when lat, lon, zoom and accessKey is provided
        x_tyle,y_tyle = self.ret_xy_tiles(lat_deg,lon_deg)
        return [x_tyle,y_tyle]
    
    def get_img(self,url_str):
        # to get the images from the url provided and save it
        global headers, LOCK_VAR, UNLOCK_VAR, LOCKING_LIMIT
        print(url_str)
        UNLOCK_VAR = UNLOCK_VAR + 1
        LOCK_VAR = 1
        print("UNLOCK VAR : ",UNLOCK_VAR)
        if UNLOCK_VAR >= LOCKING_LIMIT:
            LOCK_VAR = 0
            UNLOCK_VAR = 0
            print("-------- UNLOCKING")
        x_tyle = url_str[0]
        y_tyle = url_str[1]
        file_name = str(x_tyle)+"_"+str(y_tyle)+".jpeg"
        
        if open(str(file_name),'r') == True:
            pass
        else:
            try:
                req_url = str("https://sat-cdn"+str(1)+".apple-mapkit.com/tile?style=7&size=1&scale=1&z="+str(self.zoom)+"&x="+str(x_tyle)+"&y="+str(y_tyle)+"&v=4072"+str(self.ac_key))
                print(req_url)
                r = requests.get(req_url, #allow_redirects=True,
                                headers=headers)
                open(file_name, 'wb').write(r.content)
                if imghdr.what(file_name) is 'jpeg':
                    print(file_name,"JPEG")
                else:
                    os.remove(file_name)
                    print(file_name,"NOT JPEG")
            except:
                print("Ops Blown Off!")
            
            try:
                req_url = str("https://sat-cdn"+str(2)+".apple-mapkit.com/tile?style=7&size=1&scale=1&z="+str(self.zoom)+"&x="+str(x_tyle)+"&y="+str(y_tyle)+"&v=4072"+str(self.ac_key))
                print(req_url)
                r = requests.get(req_url, #allow_redirects=True,
                                headers=headers)
                open(file_name, 'wb').write(r.content)
                if imghdr.what(file_name) is 'jpeg':
                    print(file_name,"JPEG")
                else:
                    os.remove(file_name)
                    print(file_name,"NOT JPEG")
            except:
                print("Ops Blown Off!")
            
            try:
                req_url = str("https://sat-cdn"+str(3)+".apple-mapkit.com/tile?style=7&size=1&scale=1&z="+str(self.zoom)+"&x="+str(x_tyle)+"&y="+str(y_tyle)+"&v=4072"+str(self.ac_key))
                print(req_url)
                r = requests.get(req_url, #allow_redirects=True,
                                headers=headers)
                open(file_name, 'wb').write(r.content)
                if imghdr.what(file_name) is 'jpeg':
                    print(file_name,"JPEG")
                else:
                    os.remove(file_name)
                    print(file_name,"NOT JPEG")
            except:
                print("Ops Blown Off!")

            try:
                req_url = str("https://sat-cdn"+str(4)+".apple-mapkit.com/tile?style=7&size=1&scale=1&z="+str(self.zoom)+"&x="+str(x_tyle)+"&y="+str(y_tyle)+"&v=4072"+str(self.ac_key))
                print(req_url)
                r = requests.get(req_url, #allow_redirects=True,
                                headers=headers)
                open(file_name, 'wb').write(r.content)
                if imghdr.what(file_name) is 'jpeg':
                    print(file_name,"JPEG")
                else:
                    os.remove(file_name)
                    print(file_name,"NOT JPEG")
            except:
                print("Ops Blown Off!")

    def download(self):
        min_lat = self.min_lat_deg
        max_lat = self.max_lat_deg
        min_lon = self.min_lon_deg
        max_lon = self.max_lon_deg
        if min_lat > max_lat:
            i_val = -1
        else:
            i_val = 1
        
        if max_lon > max_lon:
            j_val = -1
        else:
            j_val = 1
        URL_ALL = []
        for i in tqdm(np.arange(float(min_lat),float(max_lat),i_val*0.0005)):
            
            for j in np.arange(float(min_lon),float(max_lon),j_val*0.0005):
                get_urls = self.make_url(i,j)
                URL_ALL.append([get_urls[0],get_urls[1]])
                #URL_ALL.append([2,get_urls[0],get_urls[1]])
                #URL_ALL.append([3,get_urls[0],get_urls[1]])
                #URL_ALL.append([4,get_urls[0],get_urls[1]])
        print("ALL URL CREATED! ...")
        global LOCK_VAR, UNLOCK_VAR, LOCKING_LIMIT
        if LOCK_VAR == 0:
            print("LOCKING")
            LOCK_VAR = 1
            UNLOCK_VAR = 0
            ThreadPool(LOCKING_LIMIT).imap_unordered(self.get_img, URL_ALL)