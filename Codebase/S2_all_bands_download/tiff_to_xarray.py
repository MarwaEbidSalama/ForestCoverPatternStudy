import os
import xarray as xr
import warnings
import numpy as np
import scipy
import rasterio
from rasterio.merge import merge
from rasterio.features import geometry_mask
import geopandas as gpd


date = os.listdir('/work/users/jn906hluu/S2_Frankenwald_daily_HD')[0]

rgb_path = f'/work/users/jn906hluu/S2_Frankenwald_daily_HD/{date}'
cm_path = f'/work/users/jn906hluu/S2_Frankenwald_daily_HD_CM/{date}'

crs_path = '/work/users/jn906hluu/S2_Frankenwald_daily/2019_03_17/response.tiff'
shape_file_path = '/work/users/jn906hluu/RSP/ForestCoverPatternStudy/Layers/D48/D48.shp'
example_path = '/work/users/jn906hluu/example.tif'

output_path = '/work/users/jn906hluu/S2_Frankenwald_nc/'

# list of dataarrays

dataarrays_rgb = [rasterio.open(f'{os.path.join(folder)}/response.tiff') for folder in os.scandir(rgb_path) if os.path.isdir(folder)]
dataarrays_cm = [rasterio.open(f'{os.path.join(folder)}/response.tiff') for folder in os.scandir(cm_path) if os.path.isdir(folder)]

merged_rgb = merge(dataarrays_rgb)
merged_cm = merge(dataarrays_cm)

len_band, len_lat, len_lon, = merged_rgb[0].shape
_, len_lat_cm, len_lon_cm, = merged_cm[0].shape

bbox = [10.294189,50.307024,11.961365,50.972242]

xrds_rgb = xr.Dataset(
    data_vars = dict(
        refl = (['band','lat', 'lon'], merged_rgb[0])
    ),
    coords = dict(
        lat = np.linspace(bbox[3], bbox[1], len_lat),
        lon = np.linspace(bbox[0], bbox[2], len_lon),
        band = np.arange(1, len_band + 1),
    ),
)

xrds_mask = xr.Dataset(
    data_vars = dict(
        mask = (['lat', 'lon'], merged_cm[0][0 , : ,:] / 255)
    ),
    coords = dict(
        lat = np.linspace(bbox[3], bbox[1], len_lat_cm),
        lon = np.linspace(bbox[0], bbox[2], len_lon_cm),
    ),
)

new_lat = np.linspace(bbox[3], bbox[1], 7530)
new_lon = np.linspace(bbox[0], bbox[2], 11540)

if (len(xrds_rgb.lat) != 7530) or (len(xrds_rgb.lon) != 11540) :

    xrds_rgb = xrds_rgb.interp(lat=new_lat, lon=new_lon)

xrds_rgb['mask'] = xrds_mask.interp(lat=new_lat, lon=new_lon).mask


shapefile = gpd.read_file(shape_file_path)


# Open the raster file
with rasterio.open(crs_path) as src:
    raster_crs = src.crs

with rasterio.open(example_path) as src:

    # Get the CRS of the raster file
    # Get the shape of the raster file
    raster_shape = xrds_rgb.mask.shape

    shapefile = shapefile.to_crs(raster_crs)
    # Get the transform of the raster file
    raster_transform = src.transform
    geometry = shapefile.geometry
    # Create a mask from the geometry
    mask_tw = geometry_mask([geometry[0]], raster_shape, raster_transform, invert=True)
    mask_fw = geometry_mask([geometry[1]], raster_shape, raster_transform, invert=True)
    mask_all = ~mask_fw & ~mask_tw

boolean_cloud_mask = xrds_rgb['mask'].astype('bool')

xrds_rgb['mask'] = ~(mask_all | boolean_cloud_mask)


xrds_rgb.to_netcdf(f'{output_path}{date}.nc')