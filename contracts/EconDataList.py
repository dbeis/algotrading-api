from typing import List
from .EconDataRecord import *
import json

class EconDataListRequest(object):
    def __init__(self, data: List[EconData]) -> None:
        self.data = data
            
    @classmethod
    def from_json(cls, data):
        x = list(map(EconData.from_json, data['data']))
        return cls(x)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

class EconDataListResponse(object):
    def __init__(self, data: List[EconDataResponse]) -> None:
        self.data = data
            
    @classmethod
    def from_json(cls, data):
        x = list(map(EconDataResponse.from_json, data['data']))
        return cls(x)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

