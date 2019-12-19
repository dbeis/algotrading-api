from typing import List
import json


class CrawledTwitterData(object):

    def __init__(self, cid: str, content: str, timestamp: int, tags: List[str]) -> None:
        self.cid = cid
        self.content = content
        self.timestamp = timestamp
        self.tags = tags
    
    @classmethod
    def from_json(cls, data):
        return cls(**data)


class CrawledTwitterDataResponse(object):

    def __init__(self, cid: str, content: str, timestamp: int) -> None:
        self.cid = cid
        self.content = content
        self.timestamp = timestamp
    
    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def serialize(self):
        return json.dumps(self.__dict__)
