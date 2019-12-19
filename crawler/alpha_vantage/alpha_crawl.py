from ..common import post_econ_data
from contracts.EconDataRecord import EconData
from contracts.EconDataList import EconDataListRequest

import time 
import json
from discord import *
import pandas

def get_stock(name, api_key):
    eq_url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}&datatype=csv".format(name, api_key)

    try:
        temp_data=pandas.read_csv(eq_url)
    except:
        warning_update("{} equity could not be downloaded".format(name))
        return False

    if temp_data.shape[0]>10:
        print(name+"\t\t\t--success!")
        post_frame(temp_data, name)
        return True
    else:
        print(name+"\t--XX .too few lines or empty")
        warning_update("{} - file had too few lines".format(name))
        return False


def post_frame(data_frame, name):
    post_list=[]
    for _, row in data_frame.iterrows():
        post_list.append(
            EconData(
                row['timestamp'],
                name,
                row['open'],
                row['close'],
                row['high'],
                row['low'],
                row['volume']
            )
        )
    
    data_list = EconDataListRequest(post_list)

    try:
        response = post_econ_data(data_list)
        if response.status_code != 200:
            raise Exception(f'Got not-OK status code {response.status_code}.')
        # success
    except BaseException as e:
        print(str(e))
        notify('crawler', human_required_update(str(e), 'twitter'))
        return
        
