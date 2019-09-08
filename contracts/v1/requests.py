from typing import List
import json

class CrawledSocialDataRecord(object):

    def __init__(self, cid: str, content: str, timestamp: float, tags: List[str]) -> None:
        self.cid = cid
        self.content = content
        self.timestamp = timestamp
        self.tags = tags
    
    @classmethod
    def from_json(cls, data):
        return cls(**data)

        
class CrawledSocialDataRequest(object):

    def __init__(self, data: List[CrawledSocialDataRecord]) -> None:
        self.data = data

    @classmethod
    def from_json(cls, data):
        students = list(map(CrawledSocialDataRecord.from_json, data['data']))
        return cls(students)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    