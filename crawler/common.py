import requests as req
from contracts import *

BASE_URL = "http://localhost:8080"


def fetch_social_progress():
    return req.get(url = BASE_URL + '/api/crawler/latest')

def post_social_data(data: CrawledSocialDataRequest):
    return req.post(url = BASE_URL + '/api/crawler/insert', data=data.serialize())

