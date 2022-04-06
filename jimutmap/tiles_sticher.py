
# ======================================================
# This program stitches tiles fetched by jimutmap.
# Note this doesnot uses multi-processing 
# OPEN SOURCED UNDER GPL-V3.0.
# Author : Jimut Bahan Pal | jimutbahanpal@yahoo.com
# Project Website: https://github.com/Jimut123/jimutmap
# ======================================================

import cv2
import ssl
import os
import time
import math
import glob
import imghdr
import requests
import sqlite3
import numpy as np
import datetime as dt
from tqdm import tqdm
import multiprocessing
from jimutmap import api
from typing import Tuple
from selenium import webdriver
import chromedriver_autoinstaller
from multiprocessing.pool import ThreadPool
from os.path import join, exists, normpath, relpath


def update_stitcher_db(folder_name = "myOutputFolder"):
    # this function stiches the whole folder passed to it
    
    # to take the files present in the folder and update all the entries of the 
    # sticher database

    # Create table sticher with the coordinates, and the corresponding
    # satellite tile and the road tile, id as the primary key xTile_yTile

    cur.execute('''CREATE TABLE IF NOT EXISTS sticher
                (id TEXT primary key, xTile INTEGER, yTile INTEGER, satellite_tile INTEGER, road_tile INTEGER )''')
    
    print("Updating sticher db ...")

    all_files_folder = glob.glob('{}/*'.format(folder_name))
    for tile_name in tqdm(all_files_folder):
        if tile_name.count('_') == 1:
            # then it is a satellite imagery
            xTile_val = str(tile_name.split('_')[0]).split('/')[-1]
            yTile_val = str(tile_name.split('_')[-1]).split('.')[0]
            create_id = str(xTile_val)+"_"+str(yTile_val)
            # print(create_id)
            
            # create the primary key for tracking values
            key_id = str(xTile_val)+"_"+str(yTile_val)
            # write the query
            query_insert = "INSERT OR IGNORE INTO sticher VALUES ('{}','{}','{}','{}','{}')".format(key_id,xTile_val, yTile_val, 0, 0)
            # Insert a row of records
            cur.execute(query_insert)
            cur.execute('''UPDATE sticher SET satellite_tile = 1 WHERE id = ?''',(str(create_id),))	# set the satellite_tile to 1

        if tile_name.count('_') == 2:
            # then it is a road mask 
            xTile_val = str(tile_name.split('_')[0]).split('/')[-1]
            yTile_val = str(tile_name.split('_')[-2])

            # create the primary key for tracking values
            key_id = str(xTile_val)+"_"+str(yTile_val)
            # write the query
            query_insert = "INSERT OR IGNORE INTO sticher VALUES ('{}','{}','{}','{}','{}')".format(key_id,xTile_val, yTile_val, 0, 0)
            # Insert a row of records
            cur.execute(query_insert)

            create_id = str(xTile_val)+"_"+str(yTile_val)
            # print(create_id)
            cur.execute('''UPDATE sticher SET road_tile = 1 WHERE id = ?''',(str(create_id),))	# set the road_tile to 1
    con.commit()

    get_sat_0s = cur.execute(''' SELECT * FROM sticher WHERE satellite_tile = 0 ''')
    get_sat_0s_val = cur.fetchall() #converts the cursor object to number
    total_number_of_sat0s = len(get_sat_0s_val)
    print("Total number of satellite images needed to be downloaded = ", total_number_of_sat0s)

    get_road_0s = cur.execute(''' SELECT * FROM sticher WHERE road_tile = 0 ''')
    get_road_0s_val = cur.fetchall() #converts the cursor object to number
    total_number_of_road0s = len(get_road_0s_val)
    print("Total number of satellite images needed to be downloaded = ", total_number_of_road0s)

    # in case if all the files are not present in the database then we need to exit from the program
    if total_number_of_sat0s > 0 or total_number_of_road0s > 0:
        print("Please download all the tiles properly for this purpose, some tiles may be missing...")
        print("Exiting...")
        exit()



def get_bbox_lat_lon():
    # this function obtains the maximum, minimum latitudes and longitudes present in the database
    print("Calculating bounding boxes for tiles :: ")
    get_all_data = cur.execute(''' SELECT * FROM sticher ''')
    get_all_data_vals = cur.fetchall() #converts the cursor object to number
    total_number_of_data = len(get_all_data_vals)
    print("Total number of rows present in the database= ", total_number_of_data)

    get_lat_list = []
    get_lon_list = []
    for item in tqdm(get_all_data_vals):
        get_lat_list.append(item[1])
        get_lon_list.append(item[2])
    
    min_lat = min(get_lat_list)
    max_lat = max(get_lat_list)

    min_lon = min(get_lon_list)
    max_lon = max(get_lon_list)

    print("Min lat tile = {}, Max lat tile = {}, Min lon tile = {}, Max lon tile = {}".format(min_lat, max_lat, min_lon, max_lon))

    return [min_lat, max_lat, min_lon, max_lon]


def stitch_whole_tile(save_name="full_tile", folder_name="myOutputFolder"):
    # This function stitches the whole tile and saves in <save_name>_sat.png and <save_name>_road.png
    # firstly update the stitcher databse
    update_stitcher_db(folder_name="myOutputFolder")

    # get the bounding box
    min_lat, max_lat, min_lon, max_lon = get_bbox_lat_lon()

    diff_lat = max_lat - min_lat
    diff_lon = max_lon - min_lon

    print("No. of tiles in latitude = {}, and longitude = {}".format(diff_lat, diff_lon))

    print("Creating an image of size : {}x{} pixels ...".format(diff_lat*256,diff_lon*256))

    # stich the satellite imagery tile

    SAT_TILE_FULL = np.zeros([diff_lon*256,diff_lat*256,3])

    for lat in tqdm(range(min_lat, max_lat)):
        for lon in range(min_lon, max_lon):
            # stich the tiles together
            img_name = folder_name+"/"+str(lat)+"_"+str(lon)+".jpg"
            sat_img = cv2.imread(img_name)
            # print(sat_img.shape)
            x_1 = int(256*(lat-min_lat+1))-256
            x_2 = int(256*(lat-min_lat+1))

            y_1 = int(256*(lon-min_lon+1)-256)
            y_2 = int(256*(lon-min_lon+1))
            # print(x_1," ",x_2," ",y_1," ",y_2)
            SAT_TILE_FULL[y_1:y_2, x_1:x_2] = sat_img
    
    sat_save_name = save_name+"_sat.png"
    cv2.imwrite(sat_save_name,SAT_TILE_FULL)

    # stich the road imagery tile

    ROAD_TILE_FULL = np.zeros([diff_lon*256,diff_lat*256,3])

    for lat in tqdm(range(min_lat, max_lat)):
        for lon in range(min_lon, max_lon):
            # stich the tiles together
            img_name = folder_name+"/"+str(lat)+"_"+str(lon)+"_road.png"
            sat_img = cv2.imread(img_name)
            # print(sat_img.shape)
            x_1 = int(256*(lat-min_lat+1))-256
            x_2 = int(256*(lat-min_lat+1))

            y_1 = int(256*(lon-min_lon+1)-256)
            y_2 = int(256*(lon-min_lon+1))
            # print(x_1," ",x_2," ",y_1," ",y_2)
            ROAD_TILE_FULL[y_1:y_2, x_1:x_2] = sat_img
    
    sat_save_name = save_name+"_road.png"
    cv2.imwrite(sat_save_name,ROAD_TILE_FULL)







# connect to the temporary database that we shall use
con = sqlite3.connect('sticher.sqlite')
cur = con.cursor()

if __name__ == "__main__":
    # use main function for proper structuing of code
    update_stitcher_db("myOutputFolder")