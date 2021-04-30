.. jimutmap documentation master file, created by
   sphinx-quickstart on Thu Apr 29 18:54:11 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

jimutmap Documentation
#########################

API to get enormous amount of high resolution satellite images from apple maps quickly through multi-threading! create map your own map dataset. 
This manually brute forces `apple-map <https://satellites.pro/#32.916485,62.578125,4)>`_. It Then scraps all the tiles (image and road mask pair) as given by the 
parameters provided by the user. This uses an API-key generated at the time of browsing the map. 

The api `accessKey` token is automatically fetched if you have Google Chrome or Chromium installed using `chromedriver-autoinstaller`. 
Otherwise, you'll have to fetch it manually and set the `ac_key` parameter (which can be found out by selecting one tile from Apple Map, 
through chrome/firefox by going Developer->Network, looking at the assets, and finding the part of the link beginning with `&accessKey=` until 
the next `&`) every 10-15 mins. 

*version*: |version|

Requirements
============
* `certifi  <https://pypi.org/project/certifi/>`_
* `chardet <https://pypi.org/project/chardet/>`_
* `chromedriver-autoinstaller <https://pypi.org/project/chromedriver-autoinstaller/>`_
* `idna <https://pypi.org/project/idna/>`_
* `numpy <https://pypi.org/project/numpy/>`_
* `requests <https://pypi.org/project/requests/>`_
* `selenium <https://pypi.org/project/selenium/>`_
* `tqdm <https://pypi.org/project/tqdm/>`_
* `urllib3 <https://pypi.org/project/urllib3/>`_

Why jimutmap?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Well it's good (best in the world) satellite images, we just need to give the coordinates (Lat,Lon, and zoom) to get your dataset
of high resolution satellite images! Create your own dataset and apply ML algorithms :')




Standard pip install
====================

.. code-block:: bash

   sudo pip3 install jimutmap

The scraping API is present, call it and download it.

.. code-block:: python3
	
	from jimutmap import api

	download_obj = api(min_lat_deg = 10,
					max_lat_deg = 10.2,
					min_lon_deg = 10,
					max_lon_deg = 11,
					zoom = 19,
					verbose = False,
					threads_ = 5, 
					container_dir = "myOutputFolder")

	# If you don't have Chrome and can't take advantage of the auto access key fetch, set
	# a.ac_key = ACCESS_KEY_STRING
	# here

	download_obj.download(getMasks = True)


.. note::

	This also uses multithreading, which may overload your computer, so set the parameters in the API, minimise the pool else your PC may hang! This is created for educational and research purposes only! The `authors <https://github.com/Jimut123/jimutmap/blob/master/CONTRIBUTORS.md>`_ are not liable for any damage to private property.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

