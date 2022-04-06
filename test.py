
# ======================================================
# This tests the working of jimutmap package.
# Note this doesnot uses multi-processing 
# OPEN SOURCED UNDER GPL-V3.0.
# Author : Jimut Bahan Pal | jimutbahanpal@yahoo.com
# Project Website: https://github.com/Jimut123/jimutmap
# ======================================================

# Using map tiles for Kolkata, my hometown!

import os
import glob
import shutil
from jimutmap import api, sanity_check, stitch_whole_tile


download_obj = api(min_lat_deg = 22.35,
                      max_lat_deg = 22.36,
                      min_lon_deg = 88.0,
                      max_lon_deg = 88.01,
                      zoom = 19,
                      verbose = False,
                      threads_ = 50, 
                      container_dir = "myOutputFolder")

# If you don't have Chrome and can't take advantage of the auto access key fetch, set
# a.ac_key = ACCESS_KEY_STRING
# here

# getMasks = False if you just need the tiles 
download_obj.download(getMasks = True)

# create the object of class jimutmap's api
sanity_obj = api(min_lat_deg = 22.35,
                      max_lat_deg = 22.36,
                      min_lon_deg = 88.0,
                      max_lon_deg = 88.01,
                      zoom = 19,
                      verbose = False,
                      threads_ = 50, 
                      container_dir = "myOutputFolder")

sanity_check(min_lat_deg = 22.35,
                max_lat_deg = 22.36,
                min_lon_deg = 88.0,
                max_lon_deg = 88.01,
                zoom = 19,
                verbose = False,
                threads_ = 50, 
                container_dir = "myOutputFolder")

print("Cleaning up... hold on")

sqlite_temp_files = glob.glob('*.sqlite*')

print("Temporary sqlite files to be deleted = {} ? ".format(sqlite_temp_files))
inp = input("(y/N) : ")
if inp == 'y' or inp == 'yes' or inp == 'Y':
    for item in sqlite_temp_files:
        os.remove(item)



## Try to remove tree; if failed show an error using try...except on screen
try:
    chromdriver_folders = glob.glob('[0-9]*')
    print("Temporary chromedriver folders to be deleted = {} ? ".format(chromdriver_folders))
    inp = input("(y/N) : ")
    if inp == 'y' or inp == 'yes' or inp == 'Y':
        for item in chromdriver_folders:
            shutil.rmtree(item)
except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))



# update_stitcher_db("myOutputFolder")
# get_bbox_lat_lon()
stitch_whole_tile(save_name="Kolkata", folder_name="myOutputFolder")