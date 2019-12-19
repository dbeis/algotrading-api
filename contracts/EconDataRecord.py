import json

class EconData(object):
    def __init__ (self, timestamp:float, equity:str, open_price:float, close_price:float, high_price:float, low_price:float, volume:int):
        self.timestamp = timestamp
        self.equity = equity
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.volume = volume
    
    @classmethod
    def from_json(cls, data):
        return cls(**data)


class EconDataResponse(object):
    def __init__ (self, cid: int, timestamp:float, equity:str, open_price:float, close_price:float, high_price:float, low_price:float, volume:int):
        self.cid = cid 
        self.timestamp = timestamp
        self.equity = equity
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.volume = volume
    
    @classmethod
    def from_json(cls, data):
        return cls(**data)
    
    def serialize(self):
        return json.dumps(self.__dict__)