from typing import List
from .CrawledDataRecord import *
import json

class CrawledDataListRequest(object):

    def __init__(self, data: List[CrawledData]) -> None:
        self.data = data

    @classmethod
    def from_json(cls, data):
        x = list(map(CrawledData.from_json, data['data']))
        return cls(x)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


class CrawledDataListResponse(object):

    def __init__(self, data: List[CrawledDataResponse]) -> None:
        self.data = data

    @classmethod
    def from_json(cls, data):
        x = list(map(CrawledDataResponse.from_json, data['data']))
        return cls(x)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
