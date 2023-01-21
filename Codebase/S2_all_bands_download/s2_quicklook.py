import os 
import rasterio 
import matplotlib.pyplot as plt
import datetime
import numpy as np
from tqdm import tqdm

path = '/work/users/jn906hluu/S2_Frankenwald_daily/'
list_dir = os.listdir(path)

quicklook_dir = '/work/users/jn906hluu/to_gif_daily/'

for folder in tqdm(list_dir):
    
    image_path = path + folder + '/response.tiff'



    with rasterio.open(image_path) as dataset:
        red_channel = dataset.read(4) / 25500
        green_channel = dataset.read(3) / 25500
        blue_channel = dataset.read(2) / 25500

        plt.imshow(7.5 * np.dstack((red_channel, green_channel, blue_channel)))
        plt.savefig(f'{quicklook_dir}{folder}.png')
