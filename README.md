 <h1 align='center'> jimutmap </h1>
<div align="center">
<a href="https://pypi.org/project/jimutmap/"><img src="https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&type=6&v=1.3.7"></a>
<a href="https://zenodo.org/badge/latestdoi/169246557"><img src="https://zenodo.org/badge/169246557.svg" alt="DOI"></a>
<a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPL%20v3-blue.svg"></a>
<img src="https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg">
<img src="https://badges.frapsoft.com/os/v1/open-source.png?v=103">
<a href="https://colab.research.google.com/github/Jimut123/jimutmap/blob/master/maps_scraper.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
</div>

## Purpose 

This manually brute forces [apple-map](https://satellites.pro/#32.916485,62.578125,4). It Then scraps all the tiles (image and road mask pair) as given by the 
parameters provided by the user. This uses an API-key generated at the time of browsing the map. 

The api `accessKey` token is automatically fetched if you have Google Chrome or Chromium installed using `chromedriver-autoinstaller`. Otherwise, you'll have to fetch it manually and set the `ac_key` parameter (which can be found out by selecting one tile from Apple Map, through chrome/firefox by going Developer->Network, looking at the assets, and finding the part of the link beginning with `&accessKey=` until the next `&`) every 10-15 mins. 

## Some of the example images downloaded at different scales

| | | | |
|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|
| <img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/1_urban_map_sat.jpeg"> | <img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/1_urban_map_mask.png"> | <img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/different_zoom_map.jpeg">|<img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/different_zoom_mask.png">|
|<img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/higher_scale_map.jpeg">  |  <img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/higher_scale_mask.png">|<img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/map_us_1.jpeg">|<img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/mask_us_1.png">|
|<img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/raj_map_1.jpeg">  |  <img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/raj_mask_1.png">|<img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/us_1_map.jpeg">|<img width="1604" src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/us_1_mask.png">|

## YouTube video 

If you are confused with the documentation, please see this video, to see the scraping in action [Apple Maps API to get enormous amount of satellite data for free using Python3](https://www.youtube.com/watch?v=voH0qhGXfsU).



## Installation

```
sudo pip install jimutmap
```

## Sample of the images downloaded

<center>
<a href="https://www.youtube.com/watch?v=wCbZhtWe72w" alt="yt video" target="_blank"><img src="https://raw.githubusercontent.com/Jimut123/jimutmap/master/satellite_data/scrn.png" alt="img of sat dat" width=85% height=85%></a>
</center>

#### Download the whole dataset [https://drive.google.com/u/3/uc?id=1-2LeYNZquto5vZlDnyuIxXhTzBh2EjRp](https://drive.google.com/u/3/uc?id=1-2LeYNZquto5vZlDnyuIxXhTzBh2EjRp).

## Need for scraping satellite data

Well it's good (best in the world) satellite images, we just need to give the coordinates (Lat,Lon, and zoom) to get your dataset
of high resolution satellite images! Create your own dataset and apply ML algorithms :')



The scraping API is present, call it and download it.
```python
>>from jimutmap import api
>>a=api(min_lat_deg,max_lat_deg,min_lon_deg,max_lon_deg,zoom=19,verbose=False,threads_=110, container_dir= "myOutputFolder")

# If you don't have Chrome and can't take advantage of the auto access key fetch, set
# a.ac_key = ACCESS_KEY_STRING
# here

>>a.download(getMasks=True)

100%|██████████████████████████████████████████████████████████████                     | 1000/10000000 [00:02<00:00, 3913.19it/s

```

#### Perks 

Well I'm not that bad. This is done through parallel proccessing, so this will take all the thread in your CPU, change the 
code to your own requirements! This is done so that you could download about **40K** images in **30 mins!** (That's too fast!!!)

If you want to re-fetch tiles, remember to delete/move tiles after every fetch request done! Else you won't get the updated information (tiles) of satellite data after
that tile. It is calculated automatically so that all the progress remains saved!


## Additional Note

This also uses multithreading, which may overload your computer, so set the parameters in the API, minimise the pool else your PC may hang! 
**This is created for educational and research purposes only! The author is not liable for any damage to private property.**


## Contribution


Please feel free to raise issues and fix any existing ones. Further details can be found in our [code of conduct](https://github.com/Jimut123/jimutmap/blob/master/CODE_OF_CONDUCT.md).

### While making a PR, please make sure you:
- [ ] Always start your PR description with "Fixes #issue_number", if you're fixing an issue.
- [ ] Briefly mention the purpose of the PR, along with the tools/libraries you have used. It would be great if you could be version specific.
- [ ] Briefly mention what logic you used to implement the changes/upgrades.
- [ ] Provide in-code review comments on GitHub to highlight specific LOC if deemed necessary.
- [ ] Please provide snapshots if deemed necessary.
- [ ] Update readme if required.

## [LICENSE](https://github.com/Jimut123/jimutmap/blob/master/LICENSE)
```
 GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2019-20 Jimut Bahan Pal, <https://jimut123.github.io/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
```

# BibTeX and citations

```
@misc{jimutmap_2019,
  author = {Jimut Bahan Pal},
  title = {jimutmap},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Jimut123/jimutmap}},
}
```



