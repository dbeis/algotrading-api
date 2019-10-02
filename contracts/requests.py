from typing import List
import json
#Todo: Bad practice fix Decouple the request class -> Per object requests/responses.
class CrawledData(object):

    def __init__(self, cid: str, content: str, timestamp: float, tags: List[str]) -> None:
        self.cid = cid
        self.content = content
        self.timestamp = timestamp
        self.tags = tags
    
    @classmethod
    def from_json(cls, data):
        return cls(**data)

        