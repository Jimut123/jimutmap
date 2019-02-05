"""
    Dated : 4/2/2018
    API to get the satellite images of apple_maps
    author : jimutbahanpal@yahoo.com
    
    After downloading, perform this 
        :=>$ mv *.jpeg satellite_data

    To get the acess-key 
    go to https://satellite.org and go to Networks (ctrl+shift+E) 
    copy the access key from &access
    paste it!
    eg : &accessKey=1549286582_4855796152370621808_%2F_FCw15IokJ0a9Y6XLiflel4UEMXTqQQf3Ya4G4xcJkbU%3D&emphasis=standard&tint=dark
    This parameter changes everytime!
"""
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

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cdn = [1,2,3,4]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'#,
    #'From': 'youremail@domain.com'  # This is another valid field
}
"""
from satcdnApplScrap import api
a =api()
a.
"""

class api:

    def ret_xy_tiles(self,lat_deg,lon_deg,zoom=19):
        # changes for 0.0005
        # This function returns the tilex and tiley in tuple
        # Takes latitude, longitude and zoom_level
        n = 2**zoom
        xtile = n * ((lon_deg + 180) / 360)
        lat_rad = lat_deg * math.pi / 180.0
        ytile = n * (1 - (math.log(math.tan(lat_rad) + 1/math.cos(lat_rad)) / math.pi)) / 2
        return int(xtile),int(ytile)

    def ret_lat_lon(self,x_tyle,y_tyle,zoom=19):
        # This function returns the lat, lon as a tuple
        # Takes x_tyle, y_tyle and zoom_level
        n = 2**zoom
        lon_deg = int(x_tyle)/n * 360.0 - 180.0
        lat_rad = math.atan(math.asinh(math.pi * (1 - 2 * int(y_tyle)/n)))
        lat_deg = lat_rad * 180.0 / math.pi
        return lat_deg, lon_deg

    def make_url(self,lat_deg,lon_deg,access_Key,zoom=19):
        # returns the list of urls when lat, lon, zoom and accessKey is provided
        x_tyle,y_tyle = self.ret_xy_tiles(lat_deg,lon_deg,zoom)
        get_url = []
        for i in cdn:
            get_url.append(str("https://sat-cdn"+str(i)+".apple-mapkit.com/tile?style=7&size=1&scale=1&z=19&x="+str(x_tyle)+"&y="+str(y_tyle)+"&v=4002"+str(access_Key)))
        return get_url
    
    def get_img(self,url_str):
        # to get the images from the url provided and save it
        global headers
        try:
            x_ = url_str.find('&x=')
            y_ = url_str.find('&y=')
            v_ = url_str.find('&v=')
            x_tyle = url_str[x_+3:y_]
            y_tyle = url_str[y_+3:v_]
            file_name = str(x_tyle)+"_"+str(y_tyle)+".jpeg"
            r = requests.get(url_str, #allow_redirects=True,
                            headers=headers)
            open(file_name, 'wb').write(r.content)
            if imghdr.what(file_name) is 'jpeg':
                print(file_name,"JPEG")
            else:
                os.remove(file_name)
                print(file_name,"NOT JPEG")
        except:
            print("Ops Blown Off!")
        
    def check_data(self,zoom=19):
        # This function returns the maximum of pic 
        # lat,lon number present in the satellite folder
        try:
            mypath = "./satellite_data"
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            max_file = max(onlyfiles)
            #print()
            print(max_file)
            _ = max_file.find('_')
            jp = max_file.find('.jpeg')
            # got the max x_tyle number and y_tyle number
            x_tyle = max_file[:_]
            y_tyle = max_file[_+1:jp]
            # now return the lat and lon of the biggest pic present
            return self.ret_lat_lon(x_tyle,y_tyle,zoom)
        except:
            # return a tuple of 0 if not present
            print("NO FOLDER PRESENT! ... creating one!")
            directory = "satellite_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            return 0,0
    
    def download_images(self,min_lat,max_lat,min_lon,max_lon,ac_key,zoom=19):
        # returns the images from min lat => max lat and min lon => max lon
        i_l, j_l = self.check_data()
        if i_l == 0 and j_l == 0:
            print("NONE IS PRESENT... ")
            i_l = min_lat
            j_l = min_lon
        print(i_l,j_l)
        k_dum = 0
        for i in np.arange(float(i_l),float(max_lat),0.0005):
            URL_ALL = []
            for j in np.arange(float(min_lon),float(max_lon),0.0005):
                get_urls = self.make_url(i,j,ac_key,19)
                #print(get_urls)
                for item in get_urls:
                    URL_ALL.append(item)
                    k_dum+=1
                #print(URL_ALL)
        print("ALL URL CREATED! ...")
        url_part=[]
        k_ = 0
        # For fast proccessing and avoiding overloads
        for url in URL_ALL:
            url_part.append(url)
            if k_%30==0:
                ThreadPool(40).imap_unordered(self.get_img, url_part)
                url_part=[]
            k_+=1
            print("Downloading ...",k_,"/",k_dum)
                

