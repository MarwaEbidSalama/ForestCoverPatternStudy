import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import rasterio
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse

# set up the argument parser
parser = argparse.ArgumentParser(description='Plot and save images')
parser.add_argument('-n', '--ncpus', type=int, default=4,
                    help='number of cpus to use')
parser.add_argument('path', type=str, help='path to the image folders')
parser.add_argument('save_path', type=str, help='path to save the images')

# parse the arguments
args = parser.parse_args()
path = args.path
quicklook_dir = args.save_path
ncpus = args.ncpus

print(f'Get Images from {path}')
print(f'and save them to {quicklook_dir}')

def plot_image(path):
    image_path = path + '/response.tiff'
    print(image_path)
    with rasterio.open(image_path) as dataset:

        red_channel = dataset.read(4) / 10000 * 3.5
        green_channel = dataset.read(3) / 10000 * 3.5
        blue_channel = dataset.read(2) / 10000 * 3.5

        plt.imshow(np.dstack((red_channel, green_channel, blue_channel)))
        print('plotted!')
        plt.savefig(quicklook_dir + f'{path[-10:]}.png')
        print('save output to:')
        print(quicklook_dir + f'{path[-10:]}.png')


with ProcessPoolExecutor(max_workers=ncpus) as executor:
    tasks = [executor.submit(plot_image, os.path.join(folder)) for folder in os.scandir(path) if folder.is_dir()]
    for f in tqdm(as_completed(tasks), total=len(tasks)):
        pass