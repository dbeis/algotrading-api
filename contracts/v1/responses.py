from typing import List
import json 

class CrawledSocialDataRecordResponse(object):

    def __init__(self, cid: str, content: str, timestamp: float) -> None:
        self.cid = cid
        self.content = content
        self.timestamp = timestamp
    
    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def serialize(self):
        return json.dumps(self.__dict__)
    
class CrawledSocialDataResponse(object):

    def __init__(self, data: List[CrawledSocialDataRecordResponse]) -> None:
        self.data = data

    @classmethod
    def from_json(cls, data):
        x = list(map(CrawledSocialDataRecordResponse.from_json, data['data']))
        return cls(x)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
