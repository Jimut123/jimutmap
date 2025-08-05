#### Here are the list of todos **(Open an issue if you want to contribute!)**:


- [ ] Stitch tiles by specifying length and breadth of tiles. 
- [ ] Get roads route in json format from specified latitude longitudes, this can help the data scientists to create optimal routes from point A to B.
- [ ] Convert all the class of objects present in the map to JSON data via image processing, which can help the geoscientists to process information at a large scale.
- [ ] Find all the unique items that can be present in the map. (Like caffe icon, shop icon, temple icon etc.)
- [ ] Fetch all the necessary objects (shops/caffe etc.) that are queried to in a certain radius of coordinate.
- [ ] Probably use other 3D data to create 3D world from satellite 2D imagery.
- [ ] Create a conda package

#### Done

- [x] Generate a high resolution map by assembling tiles, similar to [label-maker](https://github.com/developmentseed/label-maker).
- [x] Probably make a documentation website similar to 
  - [ ] [GPy](https://gpy.readthedocs.io) 
  - [x] [requests](https://requests.readthedocs.io) -- with Sphinx theme
  - [ ] [AX](https://ax.dev/) 


------------------------------------------------------------------------------

Note:

* Probably create a separate module for all these stuffs

* Also create a separate branch like **feature-name** for each feature, and then after all the tests
 and stuffs, merge them to master branch. 
 
* Maintain the [CHANGELOG.md](https://github.com/Jimut123/jimutmap/blob/master/CHANGELOG.md) in a detailed way from now onwards (Only add significant changes after deploying to master)

* After a feature is deployed to master, [x] it here.

* Master should always contain production-ready code for deployment to pip and conda
