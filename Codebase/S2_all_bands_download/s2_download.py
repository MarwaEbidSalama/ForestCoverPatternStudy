###    The script defines a function get_all_bands_request(time_interval) that takes a time_interval as input
###    and returns a SentinelHubRequest object with the specified parameters for image acquisition:
###
###         data_folder: the path to the folder where the images will be saved
###         evalscript: the script that defines the processing to be applied on the images
###         input_data: specifies the data collection (Sentinel2 L1C), time interval, and mosaicking order
###         responses: specifies the output format (TIFF)
###         bbox: the bounding box of the area of interest
###         size: the size of the image at the specified resolution
###         config: the instance of the SHConfig class that contains the configuration settings for Sentinel Hub services
###
###    The script creates a list of requests, one for each month, between the start and end date specified earlier 
###    using a list comprehension, each request being a call to the function get_all_bands_request(time_interval) 
###    with a specific time_interval. Then, it uses a for loop to iterate over the list of requests, download the image data 
###    for each request, and saving it to the specified data folder. The script also includes a delay of 15 seconds between 
###    consecutive requests, to avoid overloading the API.


from sentinelhub import SHConfig
import pandas as pd
import datetime
import time
from tqdm import tqdm

config = SHConfig()

if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)

evalscript_clm = """
//VERSION=3
function setup() {
  return {
    input: ["CLM"],
    output: { bands: 1 }
  }
}

function evaluatePixel(sample) {
  return [sample.CLM];
}
"""


evalscript_all_bands = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B10","B11","B12","CLM"],
                units: "DN"
            }],
            output: {
                bands: 13,
                sampleType: "INT16"
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B01,
                sample.B02,
                sample.B03,
                sample.B04,
                sample.B05,
                sample.B06,
                sample.B07,
                sample.B08,
                sample.B8A,
                sample.B09,
                sample.B10,
                sample.B11,
                sample.B12,
                sample.CLM];
    }
"""

bbox = [10.294189,50.307024,11.961365,50.972242]
resolution = 50

frankenwald_bbox = BBox(bbox=bbox, crs=CRS.WGS84)
frankenwald_size = bbox_to_dimensions(frankenwald_bbox, resolution=resolution)


start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2022, 12, 31)

list_of_requests = pd.date_range(start, end, freq= '1W').values

print(f"Image shape at {resolution} m resolution: {frankenwald_size} pixels")

def get_all_bands_request(time_interval):
    return SentinelHubRequest(
        data_folder="/work/users/jn906hluu/S2_Frankenwald_daily_CM/",
        evalscript=evalscript_clm,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=time_interval,
                mosaicking_order=MosaickingOrder.LEAST_CC,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=frankenwald_bbox,
        size=frankenwald_size,
        config=config,
    )

for i in tqdm(range(len(list_of_requests)-1)):

    t_start, t_stop = str(list_of_requests[i])[:10], str(list_of_requests[i+1])[:10]
    time_interval = (t_start, t_stop)
    print(time_interval)
    _ = get_all_bands_request(time_interval).get_data(save_data=True)
    time.sleep(5)
    print(f'downloaded image {i} of {len(list_of_requests)}')