import os
import shutil
import glob
from tqdm import tqdm


def OrderFolders(get_path):
    """
    get_path = The path of the files containing the folder
    """
    all_files = glob.glob("{}/*".format(get_path))
    for full_file_path in all_files:
        img_name = full_file_path.split('/')[-1]
        lat_folder_name = img_name.split('_')[0]
        lon_file_name = img_name.split('_')[1]
        print(lon_file_name)
        print(lat_folder_name)
        folder_path = get_path + "/" + lat_folder_name
        try:
            os.mkdir(folder_path)
        except OSError as error:
            print(error)   
        
        # get all the files containing the folder name
        glob_item = get_path+"/{}*".format(lat_folder_name)
        get_folder_files = glob.glob(glob_item)
        for files_mv in tqdm(get_folder_files):
            rename_filename = get_path+"/"+lat_folder_name+"/"+lon_file_name+"jpg"
            print("mv filename = ",files_mv)
            print(rename_filename)
            shutil.move(files_mv,rename_filename)
        break
   


if __name__ == "__main__":
    OrderFolders('../myOutputFolder')

