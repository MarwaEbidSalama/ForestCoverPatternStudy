The directory contains the following files:

- `README.md`: This file contains information about the other files in the directory, including a brief explanation of their purpose.

- `s2_download.py`: This is a Python script that downloads Sentinel-2 satellite imagery from the European Space Agency's Copernicus Open Access Hub by using the SentinelHub library. The script first sets up an SHConfig object and checks for the presence of the OAuth client ID and secret. It then imports various modules from the SentinelHub library and defines two evalscripts, one for the Cloud Mask (CLM) band and one for all bands. The script also defines a bounding box and resolution for the Frankenwald/Türingerwald  region in Germany from the `/Layers/D48.shp` shapefile. It creates a list of time intervals with a frequency of one week, between start date of 2017 and end date of 2022. The script then iterates over the list of time intervals, creates a SentinelHubRequest object for each interval and the requests are sent to the Copernicus Open Access Hub to download the images. The downloaded images are saved in the specified data folder.

- `rename.py`: This script is used to rename the folders containing the images downloaded using the `s2_download.py` script. The script starts by changing the current working directory to the folder where the images are stored.
It defines a function `get_request_dt(request_file)` that takes in a request file and reads the time from the json file.
The script then uses the glob library to get a list of all the subfolders in the current working directory. It iterates over the list of folders and for each folder it calls the get_request_dt function to extract the time from the `request.json` file. It then uses the datetime module to convert the time string to a datetime object and formats it to the desired format. The script then renames the folder to this formatted date. If the folder does not contain a request.json file, it will skip it and print 'no request.json'.

- `s2_download.ipynb`: This is a Jupyter notebook that contains the same functionality as the `s2_download.py` script, but with additional explanations and visualizations.