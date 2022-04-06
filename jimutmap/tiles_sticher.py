
# ======================================================
# This program stitches tiles fetched by jimutmap.
# OPEN SOURCED UNDER GPL-V3.0.
# Author : Jimut Bahan Pal | jimutbahanpal@yahoo.com
# Project Website: https://github.com/Jimut123/jimutmap
# ======================================================

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


def stitch_whole_folder(folder_name = "myOutputFolder"):
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





# connect to the temporary database that we shall use
con = sqlite3.connect('sticher.sqlite')
cur = con.cursor()

if __name__ == "__main__":
    # use main function for proper structuing of code
    stitch_whole_folder("myOutputFolder")