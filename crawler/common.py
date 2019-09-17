import requests as req
from contracts.v1 import *

BASE_URL = "http://localhost:8080"


def fetch_social_progress():
    return req.get(url = BASE_URL + '/api/v1/crawler/latest')

def post_social_data(data: CrawledSocialDataRequest):
    return req.post(url = BASE_URL + '/api/v1/crawler/insert', data=data.serialize())

