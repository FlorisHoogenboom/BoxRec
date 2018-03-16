import lxml.html
from .models import Fight, Boxer


class FailedToParse(Exception):
    pass


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
            FightParser.BASE_DOM_PATH + '//a[./img]/@href'
        )

        try:
            left = boxer_links[0].rsplit('/')[-1]
            right = boxer_links[1].rsplit('/')[-1]
        except IndexError:
            raise FailedToParse("Could not get boxers for fight")

        if left == '0' or right == '0':
            raise FailedToParse(
                'Fight is not complete, one of the boxers is TBA'
            )

        return left, right

    def clean_rating(self, raw):
        if raw is None:
            return None

        return int(raw.rsplit('\n')[0].replace(',',''))

    def get_rating_before_fight(self, tree):
        rating_row = tree.xpath(
            FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "before fight"]/td[position() = 1 or position() =3]'
        )
        rating_left = self.clean_rating(rating_row[0].text)
        rating_right = self.clean_rating(rating_row[1].text)

        return rating_left, rating_right
    
    def get_rating_after_fight(self, tree):
        """ New function to determine rating after fight."""
        rating_row = tree.xpath(
             FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "after fight"]/td[position() = 1 or position() =3]'  
        )
        rating_left = self.clean_rating(rating_row[0].text)
        rating_right = self.clean_rating(rating_row[1].text)

        return rating_left, rating_right

    def get_fight_outcome(self, tree, left_id, right_id):
        outcome = tree.xpath(
            FightParser.BASE_DOM_PATH + '//td[./span[@class="textWon"]]/a[./img]/@href'
        )

        try:
            winner_id = outcome[0].rsplit('/')[-1]
        except IndexError as e:
            drawn = tree.xpath(
                FightParser.BASE_DOM_PATH + '//td[./span[@class="textDrawn"]]/a[./img]/@href'
            )
            if len(drawn) > 0:
                return 'drawn'
            else:
                raise FailedToParse('Could not determine fight outcome, did it already occur?')

        if left_id == winner_id:
            return 'left'
        else:
            return 'right'

    def parse(self, response):
        tree = self.make_dom_tree(response)

        event_id, fight_id = self.get_event_and_fight_id(response.url)
        boxer_left_id, boxer_right_id = self.get_boxer_ids(tree)
        rating_before_left, rating_before_right = self.get_rating_before_fight(tree)
        rating_after_left, rating_after_right = self.get_rating_after_fight(tree)
        result = self.get_fight_outcome(tree, boxer_left_id, boxer_right_id)

        return Fight(
            event_id=event_id,
            fight_id=fight_id,
            boxer_left_id=boxer_left_id,
            boxer_right_id=boxer_right_id,
            hist_rating_left=rating_before_left,
            hist_rating_right=rating_before_right,
            curr_rating_left=rating_after_left,
            curr_rating_right=rating_after_right,
            winner=result
        )


class FightListParser(BaseParser):
    BASE_DOM_PATH = \
        '//div[@class="content"]//table[@class="calendarTable"]'

    def get_event_and_fight_ids(self, tree):
        links = tree.xpath(
            FightListParser.BASE_DOM_PATH \
                + '//td[@class="actionCell"]/div[@class="mobileActions"]/a[1]/@href'
        )

        events = map(lambda x: x.rsplit('/')[-2], links)
        fights = map(lambda x: x.rsplit('/')[-1], links)

        return events, fights


    def parse(self, response):
        tree = self.make_dom_tree(response)

        event_ids, fight_ids = \
            self.get_event_and_fight_ids(tree)

        return zip(event_ids, fight_ids)


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
