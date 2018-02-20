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
        self.index = 0
        self.search_results = []
        for page in range(1,100,10):
            params = self.params
            params['start']=page
            for item in requests.get(self.cs_uri,params).json()['items']:
                self.search_results.append(item)


    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.search_results[self.index].upper()
        except IndexError:
            raise StopIteration
        self.index += 1
        return result


c = [fight for fight in CustomSearchQuery('*')]
print(len(c))
