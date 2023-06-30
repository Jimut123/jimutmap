Parameters
==========

Here is the full list of configuration parameters you can specify when calling **api** function


**min_lat_deg**: float
	This is the minimum latitude degree that is passed to the function to capture the tiles. This may also be considered as the left boundary of the bounding box from where the scraping of tiles will start in the apple maps.

**max_lat_deg**: string
	This is the maximum latitude degree that is passed to the function to capture the tiles. This may also be considered as the right boundary of the bounding box from where the scraping of tiles will start in the apple maps.

**min_lon_deg**: string
	This is the minimum longitude degree that is passed to the function to capture the tiles. This may also be considered as the bottom boundary of the bounding box from where the scraping of tiles will start in the apple maps.

**max_lon_deg**: string
	This is the maximum longitude degree that is passed to the function to capture the tiles. This may also be considered as the top boundary of the bounding box from where the scraping of tiles will start in the apple maps.

**zoom**: string
	This is the zoom value given to the map to get the arial imagery, i.e., max = 19 (zoomed in) and min = 0 (zoomed out).

**verbose**: boolean
	This is the output that is displayed on the screen when the process is executing. This helps to keep a faith in the program by tracking the current execution.

**threads_**: integer
	Set according to the number of cores present in your current CPU. Recommended value is **4**. The more the value, the more the pressure on the CPU.

**container_dir**: string
	The container directory where the maps and the corresponding mask tiles will be stored.




Here is the full list of configuration parameters you can specify when calling **download()** function

**getMasks**: boolean
	We set it to either **True** or **False** for either downloading or not downloading corresponding road mask titles, of the same zoom value.


