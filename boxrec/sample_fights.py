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
        for page in range(1,101,10):
            params = self.params
            params['start']=page
            response = requests.get(self.cs_uri,params).json()
            if 'error' in response:
                raise Exception("[!] googleapis responded with code {0}: {1}".format(response['error']['code'],response['error']['message']))
            for item in response['items']:
                yield item

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._generator)


class CollectSampleBouts(object):
    """
    Collect a hundred fights per weight class from Google Custom query, extract the record page URI.
    """

    def __init__(self):
        self.weight_classes = [
            "Heavyweight",
            "Cruiserweight",
            "Light Heavyweight",
            "Super Middleweight",
            "Middleweight",
            "Super Welterweight",
            "Welterweight",
            "Super Lightweight",
            "Lightweight",
            "Super Featherweight",
            "Featherweight",
            "Super Bantamweight",
            "Bantamweight",
            "Super Flyweight",
            "Flyweight",
            "Light Flyweight",
            "Minimumweight"
        ]
        self._generator = self.collect_bout_uris()

    def collect_bout_uris(self):
        for weight_class in self.weight_classes:
            for result in CustomSearchQuery('{0} contest'.format(weight_class)):
                yield {
                    'weight': weight_class,
                    'url': result['link'],
                    'description':result['snippet']
                    }

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._generator)

if __name__ == '__main__':
    with open('data/fight_uri.tsv','w') as f:
        for bout in CollectSampleBouts():
            print(bout)
            f.write("{0}\t{1}\n".format(bout['url'],bout['weight']))



    print(bout)
