

# ========================================================
# This package provides useful tools for data analysts
# and geoscientists for free
# OPEN SOURCED UNDER GPL-V3.0.
# Author : Jimut Bahan Pal | jimutbahanpal@yahoo.com
# Project Website: https://github.com/Jimut123/jimutmap
# pylint: disable = global-statement
# cSpell: words imghdr, tqdm, asinh, jimut, bahan
# ========================================================

__name__ = "jimutmap"
__version__ = "1.4.1"
__author__ = "Jimut Bahan Pal | jimutbahanpal@yahoo.com"
__release_date__ = '4-May-2019'
from .jimutmap import api
from .file_size import get_folder_size
from .sanity_checker import sanity_check
from .tiles_sticher import update_stitcher_db, get_bbox_lat_lon, stitch_whole_tile
