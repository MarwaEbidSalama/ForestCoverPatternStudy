import pandas as pd
import glob
import json
import datetime as dt
from urllib.parse import unquote
import os


os.chdir('/work/users/jn906hluu/S2_Frankenwald_daily_HD/2020-05-31')

def get_request_dt(request_file):
    with open(request_file, 'r') as req:
        request = json.load(req)
        bbox = request['request']['payload']['input']['bounds']['bbox']
        return bbox
if __name__ == "__main__":
    folders = glob.glob('./*')
    dates = []
    for folder in folders:
        string_bbox = get_request_dt(f'{folder}/request.json')
        b1, b2, b3, b4 = string_bbox[0], string_bbox[1], string_bbox[2], string_bbox[3]
    
        name_formatted_bbox = f'{b1:.6f}_{b2:.6f}_{b3:.6f}_{b4:.6f}'

        print(name_formatted_bbox)
            #datetime = dt.datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%SZ')
            #name_formatted_date = datetime.strftime('%Y_%m_%d')
        os.rename(f'{folder}', name_formatted_bbox)


#    df = pd.DataFrame(zip(folders, dates), columns=['folder', 'datetime'])
#   df.sort_values(by='datetime', ascending=True, inplace=True)
#    print(df.to_markdown())
