import requests as req
from contracts.CrawledDataRecordList import *

BASE_URL = "http://localhost:8080"


def fetch_social_progress():
    return req.get(url = BASE_URL + '/api/crawler/latest')

def post_social_data(data: CrawledDataRecordListRequest):
    return req.post(url = BASE_URL + '/api/crawler/insert', data=data.serialize())

