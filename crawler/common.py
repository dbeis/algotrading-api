import requests as req
from contracts.v1 import requests, responses

BASE_URL = "http://localhost:8080"


def fetch_social_progress():
    return req.get(url = BASE_URL + '/api/v1/crawler/latest')

def post_social_data(data: requests.CrawledSocialDataRequest):
    return req.post(url = BASE_URL + '/api/v1/crawler/insert', data=data.serialize())

