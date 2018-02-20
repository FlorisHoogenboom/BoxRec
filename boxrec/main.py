import json
import requests
from config import CS_KEY, CS_CX

class CustomSearchQuery(object):
    """
    Thin Custom Search wrapper. Takes care of pagination. Max 100 results.
    """

    def __init__(self,query):
        self.cs_uri = "https://www.googleapis.com/customsearch/v1"
        self.params = {
            'key':CS_KEY,
            'cx':CS_CX,
            'q':query,
            'start':1
        }
        self._generator = self.query_gen()


    def query_gen(self):
        for page in range(1,100,10):
            params = self.params
            params['start']=page
            for item in requests.get(self.cs_uri,params).json()['items']:
                yield item

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._generator)


c = [fight for fight in CustomSearchQuery('*')]
print(len(c))
