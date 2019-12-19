from typing import List
from .CrawledTwitterDataRecord import *
import json


class CrawledTwitterDataListRequest(object):

    def __init__(self, data: List[CrawledTwitterData]) -> None:
        self.data = data

    @classmethod
    def from_json(cls, data):
        x = list(map(CrawledTwitterData.from_json, data['data']))
        return cls(x)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


class CrawledTwitterDataListResponse(object):

    def __init__(self, data: List[CrawledTwitterDataResponse]) -> None:
        self.data = data

    @classmethod
    def from_json(cls, data):
        x = list(map(CrawledTwitterDataResponse.from_json, data['data']))
        return cls(x)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
