from jimutmap import api

download_obj = api(min_lat_deg = 10,
                  max_lat_deg = 10.01,
                  min_lon_deg = 10.1,
                  max_lon_deg = 10.11,
                  zoom=19,
                  verbose=False,
                  threads_=5, 
                  container_dir= "myOutputFolder")

# If you don't have Chrome and can't take advantage of the auto access key fetch, set
# a.ac_key = ACCESS_KEY_STRING
# here
download_obj.download(getMasks=True)
