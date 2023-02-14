import xarray as xr
import os
import fsspec
from datetime import datetime

inpath = '/work/users/jn906hluu/S2_Frankenwald_zarr/'
outpath = '/work/users/my982hzao/'

list_of_dir = [os.path.join(folder) for folder in os.scandir(inpath)]

print(f'Processing {len(list_of_dir)} files...')

list_of_dir.sort()
list_of_xarray_datasets, list_of_failures = [], []
count_failed = 0

for file in list_of_dir:
    date = file.split('/')[-1].split('.')[0]
    dt = datetime.strptime(date, '%Y-%m-%d')
    try:
        ds = xr.open_zarr(fsspec.get_mapper(file), consolidated=True)
        ds = ds.assign_coords({'time' : dt})
        ds['refl'] = ds['refl'].where(ds.mask)

        #Ignoring the 13th band as this is somehow the failed cloudmask...

        list_of_xarray_datasets.append(ds.sel(band=slice(1,12)))
    except:
        count_failed += 1
        list_of_failures.append(date)

fail_ratio = count_failed / len(list_of_dir)

if fail_ratio == 0:
    print(f'Sucessfully loaded all files!')
else: 
    print(f'Failed to load {fail_ratio:.2f} of the files.')
    print(f'These files were:')
    for fail_name in list_of_failures:
        print(fail_name)

combined_set = xr.concat(list_of_xarray_datasets, dim='time').resample(time='1M').mean()

attrs = {
    "platform": "Sentinel-2",
    "product_type": "Level-2A",
    "creation_date": "2023-02-13",  
    "band_dimension": "bands",
    "band_units" : "DN",
    "band_scale_factor": 10000,
    "wavelength_units": "nanometers",
    "wavelengths": [443, 490, 560, 665, 705, 740, 783, 832, 945, 1376, 1614, 2202],
    "resolution": "10m",  # spatial resolution in meters
    "projection": "plane",  # the projection of the data
    "coordinate_reference_system": "EPSG:4326", 
    "author" : "Joshua Müller",
    "information" : "The raw data is generated from weekly Sentinel-2 images; The \
        images are masked with the D48 regionmask corresponding to the geographic area \
        of the franconian and turinga forests and a cloud maks. To avoid a high number \
        of missing values, the data is resampled to monthly resolution (corresponding to 3-4 timeslices) \
        with skip-missing (skip-na) policy.",
}

combined_set.attrs = attrs

combined_set.to_zarr(f'{outpath}S2_Frankenwald.zarr', mode='w')
