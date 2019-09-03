from typing import List

class CrawledSocialDataRecord:
    cid: str
    content: str
    timestamp: float
    tags: List[str]

    def __init__(self, cid: str, content: str, timestamp: float, tags: List[str]) -> None:
        self.cid = cid
        self.content = content
        self.timestamp = timestamp
        self.tags = tags

class CrawledSocialDataRequest:
    data: List['CrawledSocialDataRecord']
    
    def __init__(self, data: List['CrawledSocialDataRecord']) -> None:
        self.data = data
    