import pandas as pd
import glob
import json
import datetime as dt
from urllib.parse import unquote
import os


os.chdir('/work/users/jn906hluu/S2_Frankenwald_daily_CM')

def get_request_dt(request_file):
    with open(request_file, 'r') as req:
        request = json.load(req)
        time = request['request']['payload']['input']['data'][0]['dataFilter']['timeRange']['from']
        return time

if __name__ == "__main__":
    folders = glob.glob('./*')
    dates = []
    for folder in folders:
        try:
            string_date = get_request_dt(f'{folder}/request.json')

            datetime = dt.datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%SZ')
            name_formatted_date = datetime.strftime('%Y_%m_%d')
            os.rename(f'{folder}', name_formatted_date)

        except:
            print('no request.json')

#    df = pd.DataFrame(zip(folders, dates), columns=['folder', 'datetime'])
#   df.sort_values(by='datetime', ascending=True, inplace=True)
#    print(df.to_markdown())
