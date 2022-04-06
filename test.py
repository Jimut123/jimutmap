"""
Jimut Bahan Pal
First updated : 22-03-2021
Last updated : 04-04-2022
"""

import os
import glob
import shutil
from jimutmap import api, sanity_check, stitch_whole_folder


download_obj = api(min_lat_deg = 10,
                      max_lat_deg = 10.01,
                      min_lon_deg = 10,
                      max_lon_deg = 10.01,
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
sanity_obj = api(min_lat_deg = 10,
                      max_lat_deg = 10.01,
                      min_lon_deg = 10,
                      max_lon_deg = 10.01,
                      zoom = 19,
                      verbose = False,
                      threads_ = 50, 
                      container_dir = "myOutputFolder")

sanity_check(min_lat_deg = 10,
                max_lat_deg = 10.01,
                min_lon_deg = 10,
                max_lon_deg = 10.01,
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



# stitch_whole_folder("myOutputFolder")