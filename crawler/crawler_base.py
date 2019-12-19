class Crawler(object):
    """The base crawler class with the pre-defined required metadata and lifetime methods"""
    def __init__(self, config):
        self.config = config
    
    def __getitem__(self, index):
        return None

    def post(self, data):
        return None

    def __str__(self):
        return "Crawler Base"
