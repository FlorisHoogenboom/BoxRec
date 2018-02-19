import lxml.html
from .models import Fight, Boxer


class BaseParser(object):
    def __init__(self):
        pass

    def make_dom_tree(self, response):
        encoding = response.encoding
        binary_contents = response.content

        lxml_parser = lxml.html.HTMLParser(encoding=response.encoding)
        tree = lxml.html.document_fromstring(
            response.content,
            parser=lxml_parser
        )

        return tree


class FightParser(BaseParser):
    BASE_DOM_PATH = \
        '//div[@class="singleColumn"]//table[@class="responseLessDataTable"]/tr'

    def get_event_and_fight_id(self, url):
        splitted = url.rsplit('/')

        event_id = splitted[-2]
        fight_id = splitted[-1]
        return event_id, fight_id

    def get_boxer_ids(self, tree):
        boxer_links = tree.xpath(
            FightParser.BASE_DOM_PATH + '[1]//a[@class="personLink"]/@href'
        )

        left = boxer_links[0].rsplit('/')[-1]
        right = boxer_links[1].rsplit('/')[-1]

        return left, right

    def parse(self, response):
        tree = self.make_dom_tree(response)

        event_id, fight_id = self.get_event_and_fight_id(response.url)
        boxer_left_id, boxer_right_id = self.get_boxer_ids(tree)

        return Fight(
            event_id = event_id,
            fight_id = fight_id,
            boxer_left_id = boxer_left_id,
            boxer_right_id = boxer_right_id,
            winner = 'left'
        )


class BoxerParser(BaseParser):
    BASE_DOM_PATH = \
        '//div[@class="singleColumn"]//table[@class="profileTable"][1]'

    def get_boxer_id(self, url):
        return url.rsplit('/')[-1]

    def get_boxer_name(self, tree):
        return tree.xpath(
            BoxerParser.BASE_DOM_PATH + '//h1/text()'
        )[0]

    def parse(self, response):
        tree = self.make_dom_tree(response)

        boxer_id = self.get_boxer_id(response.url)
        boxer_name = self.get_boxer_name(tree)

        return Boxer(
            id = boxer_id,
            name = boxer_name
        )
