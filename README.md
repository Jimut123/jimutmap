# satcdnApplScrap

#### Purpose 

Well, someone said that [apple-map](https://satellites.pro/#32.916485,62.578125,4) is unhackable! I said yes, let me try to scrap 
data (P.S.: I'm a noob, but I'm curious). I found that it is actually not. After a 100 times of stack-overflowing and shits, I did
scrap apple-map and I'm sharing this code with you. Why am I sharing? cause I don't give a fuck to these tiny little things in this
world, neither the close source monopoly of things. 

#### First things first
Note :

The api acess-key is valid for a period of 10-15 mins. You need to manually go to [apple-map](https://satellites.pro/#32.916485,62.578125,4), get the API access key by pressing ctrl+shift+E and going to the network area. I tried to reverse engineer this thing
but couldn't. First part of the key is time in sec from 1970, but other part is some output of complex function which needs time
to decipher. If anyone finds it, let me know, I'll add you to the contributor's section and may make this API fully automatic.


#### Need for hacking and scraping satellite data

Well it's good (best in the world) satellite images, we just need to give the coordinates (Lat,Lon, and zoom) to get your dataset
of high resolution satellite images! Create your own dataset and apply ML algorithms :')

#### Some of the example images downloaded :
| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/Jimut123/apple_maps_api/blob/master/satellite_data/133478_203289.jpeg"> 
 blah |  
 <img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/Jimut123/apple_maps_api/blob/master/satellite_data/133479_203290.jpeg">|
 
 <img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/Jimut123/apple_maps_api/blob/master/satellite_data/338161_175520.jpeg">|

|<img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/Jimut123/apple_maps_api/blob/master/satellite_data/338350_175520.jpeg">  |  

<img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/Jimut123/apple_maps_api/blob/master/satellite_data/338359_175520.jpeg">|

<img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://github.com/Jimut123/apple_maps_api/blob/master/satellite_data/zoom_30/320523_197531.jpeg">|


The scraping API is present, call it and download it.
```
>>from satcdnApplScrap import api
>>a=api()

# Change the access key here
# give the (min_lat,max_lat,min_lon,max_lon,access_key) in this function
# note the access key is manually changed all the time here!

>>a.download_images(1,100,1,100,'&accessKey=1549282557_3509328514294679933_%2F_kcs5gIr9wyBn278MUbK7I55sHNmwhULq0csC3E4IFvM%3D&emphasis=standard&tint=dark')

a.download_images(40,40.5,40,40.5,'&accessKey=1549375931_5723979149709274034_%2F_iOwwf%2B70uM1bJHAEcHbkhV9zbC3RUKbTCT3LEtkJQa8%3D&emphasis=standard&tint=dark',4)
NO FOLDER PRESENT! ... creating one!
NONE IS PRESENT... 
40 40
ALL URL CREATED! ...
Downloading ... 1 / 4000000
Downloading ... 2 / 4000000
Downloading ... 3 / 4000000
Downloading ... 4 / 4000000
Downloading ... 5 / 4000000
Downloading ... 6 / 4000000
Downloading ... 7 / 4000000
Downloading ... 8 / 4000000
Downloading ... 9 / 4000000
Downloading ... 10 / 4000000
Downloading ... 11 / 4000000
Downloading ... 12 / 4000000
Downloading ... 13 / 4000000
Downloading ... 14 / 4000000
Downloading ... 15 / 4000000
Downloading ... 16 / 4000000
Downloading ... 17 / 4000000
Downloading ... 18 / 4000000
Downloading ... 19 / 4000000
Downloading ... 20 / 4000000
Downloading ... 21 / 4000000
Downloading ... 22 / 4000000
Downloading ... 23 / 4000000
Downloading ... 24 / 4000000
Downloading ... 25 / 4000000
Downloading ... 26 / 4000000
Downloading ... 27 / 4000000
320405_197531.jpeg NOT JPEG
320410_197531.jpeg NOT JPEG
320406_197531.jpeg NOT JPEG
Ops Blown Off!
Ops Blown Off!
320409_197531.jpeg NOT JPEG
Ops Blown Off!
320411_197531.jpeg NOT JPEG
Ops Blown Off!
320408_197531.jpeg NOT JPEG
320409_197531.jpeg NOT JPEG
320406_197531.jpeg NOT JPEG
Ops Blown Off!
320407_197531.jpeg NOT JPEG
320409_197531.jpeg NOT JPEG
Ops Blown Off!
320409_197531.jpeg NOT JPEG
Ops Blown Off!
320414_197531.jpeg NOT JPEG
320411_197531.jpeg NOT JPEG
Ops Blown Off!
320405_197531.jpeg NOT JPEG
Ops Blown Off!
Ops Blown Off!
Ops Blown Off!
Ops Blown Off!
320415_197531.jpeg NOT JPEG
Ops Blown Off!
Ops Blown Off!
Ops Blown Off!
Ops Blown Off!
320412_197531.jpeg NOT JPEG
320411_197531.jpeg NOT JPEG
320412_197531.jpeg NOT JPEG
Ops Blown Off!
320406_197531.jpeg NOT JPEG
```

#### Perks 

Well I'm not that bad. This is done through parallel proccessing, so this will take all the thread in your CPU, change the 
code to your own requirements! This is done so that you could download about 40K images in 30 mins! (That's fuckin fast!!!)

Do this :

```
$ mv *.jpeg satellite_data
```

To store all the JPEG images to the folder, when you will fetch the high resolution images the next time, you will get all the
images after that images, if you give the same lat,lon. So, you don't need a DB to store the update information... LOL.
But you have to do this manually everytime!


Author:
* [Jimut Bahan Pal](https://jimut123.github.io/)



