import json
import urllib.request
import pandas as pd
import numpy as np
import time
import win10toast

start_time = time.time()
toaster = win10toast.ToastNotifier()

"""
Refer to the below link to get relevent URLs for the required Harvest data
https://help.getharvest.com/api-v2/
"""

url_time = "https://api.harvestapp.com/v2/time_entries?page=1&per_page=100&ref=first"
url_estimates = "https://api.harvestapp.com/v2/estimates?page=1&per_page=100&ref=first"


"""
Replace the User-Agent, Authorization and Harvest-Account-ID details below with your details.   

Follow instructions XXX

"""

headers = {
    "User-Agent": "Harvest API Example (example@example.com.au)",
    "Authorization": "Bearer 1049503.pt.orEXgiZhPeH48BVHn1JWjuE2JDNEP4hWoWBMuaKi1hHZ6Vz71bvFETeRHN1tDv7gCXkc-FgmNw3_E8UguGY_vA",
    "Harvest-Account-ID": "1451470"
}

"""
This function pulls data using the request library, converts to JSON then creates a Pandas dataframe

You must enter the url, header and nest. The nest is the JSON nested data label contain the data for that URL
You will need to run a test query to obtain the required name of the nested data
"""


def request_pull(url, headers, nest):
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    responseBody = response.read().decode("utf-8")
    jsonResponse = json.loads(responseBody)

    time_entries_json = jsonResponse[nest]
    df = pd.json_normalize(time_entries_json, max_level=2)

    total_pages_count = jsonResponse["total_pages"]
    _links = jsonResponse["links"]
    next_page = _links.get('next')

    for i in range(int(total_pages_count)):
        if next_page is None:
            pass
        else:
            request_loop = urllib.request.Request(url=next_page, headers=headers)
            response_loop = urllib.request.urlopen(request_loop, timeout=5)
            responseBody_loop = response_loop.read().decode("utf-8")
            jsonResponse_loop = json.loads(responseBody_loop)
            nest_json_loop = jsonResponse_loop[nest]
            df_loop = pd.json_normalize(nest_json_loop)
            df = df.append(df_loop)
            _links = jsonResponse_loop["links"]
            next_page = _links.get('next')

    return df

"""
This function is similar to request_pull, however allow you to dive 1 level deeper into nested data.

It is important for the estimates data as it has multi-line level data aggregated into one field,
which needs to be expanded and merged.
"""

def request_pull_nested(url, headers, nest, nest2):
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    responseBody = response.read().decode("utf-8")
    jsonResponse = json.loads(responseBody)

    time_entries_json = jsonResponse[nest]
    df = pd.json_normalize(time_entries_json, record_path=nest2, meta='id', record_prefix=nest2+'.')

    total_pages_count = jsonResponse["total_pages"]
    _links = jsonResponse["links"]
    next_page = _links.get('next')

    for i in range(int(total_pages_count)):
        if next_page is None:
            pass
        else:
            request_loop = urllib.request.Request(url=next_page, headers=headers)
            response_loop = urllib.request.urlopen(request_loop, timeout=5)
            responseBody_loop = response_loop.read().decode("utf-8")
            jsonResponse_loop = json.loads(responseBody_loop)
            nest_json_loop = jsonResponse_loop[nest]
            df_loop = pd.json_normalize(nest_json_loop)
            df = df.append(df_loop)
            _links = jsonResponse_loop["links"]
            next_page = _links.get('next')

    return df


time_entries_df = request_pull(url_time, headers, "time_entries")
time_entries_df["project.code"] = pd.to_numeric(time_entries_df["project.code"], errors='coerce')
time_entries_df = time_entries_df.replace(np.nan, 0, regex=True)
time_entries_df["project.code"] = time_entries_df["project.code"].astype(int)

estimates_df1 = request_pull(url_estimates, headers, 'estimates')
estimates_df2 = request_pull_nested(url_estimates, headers, 'estimates', 'line_items')
estimates_df = pd.merge(estimates_df1, estimates_df2, how="left", on=["id", "id"])

time_entries_df.to_excel('./time_entries.xlsx', sheet_name='time_entries', index=False)
estimates_df.to_excel('./estimates.xlsx', sheet_name='time_entries', index=False)

script_length = "--- %s seconds ---" % (time.time() - start_time)

toaster.show_toast('Automation', 'Harvest script has successfully run, time taken '+script_length, duration=8)