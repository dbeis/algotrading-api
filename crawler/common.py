import requests as req
from contracts.CrawledDataRecordList import *
from contracts.EconDataList import EconDataListRequest

BASE_URL = "http://localhost:8080"


def fetch_social_progress():
    return req.get(url = BASE_URL + '/api/crawler/latest')

def post_social_data(data: CrawledDataListRequest):
    return req.post(url = BASE_URL + '/api/crawler/insert', data=data.serialize())

def post_econ_data(data: EconDataListRequest):
    return req.post(url = BASE_URL + '/api/crawler/insert_econ', data=data.serialize())
