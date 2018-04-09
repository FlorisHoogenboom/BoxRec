import lxml.html
from .models import Fight, Boxer
import re


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

    def extract_alphanumeric(self, raw):
        if raw is None:
            return None

        return int(raw.rsplit('\n')[0].replace(',',''))

    def get_rating_before_fight(self, tree):
        rating_row = tree.xpath(
            FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "before fight"]/td[position() = 1 or position() =3]'
        )
        rating_left = self.extract_alphanumeric(rating_row[0].text)
        rating_right = self.extract_alphanumeric(rating_row[1].text)

        return rating_left, rating_right
    
    def get_rating_after_fight(self, tree):
        """ New function to determine rating after fight."""
        rating_row = tree.xpath(
             FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "after fight"]/td[position() = 1 or position() =3]'  
        )
        rating_left = self.extract_alphanumeric(rating_row[0].text)
        rating_right = self.extract_alphanumeric(rating_row[1].text)

        return rating_left, rating_right
    
    
    def get_age(self,tree):
        """New function to retreive age of boxer. Returns None for
        values that are not included on Boxrec.com"""
        age_row = tree.xpath(
                FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "age"]/td[position() = 1 or position() = 3]'
        )
        age_left = self.extract_alphanumeric(age_row[0].text)
        age_right = self.extract_alphanumeric(age_row[1].text)
        
        return age_left, age_right
    
    def get_stance(self,tree):
        """New function to retreive stance of boxer. Returns None for
        values that are not included on Boxrec.com"""
        stance_row = tree.xpath(
                FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "stance"]/td[position() = 1 or position() = 3]'
        )
        try:
            stance_left = stance_row[0].text.rstrip()
        except AttributeError as e:
            stance_left = None

        try:
            stance_right = stance_row[1].text.rstrip()
        except AttributeError as e:
            stance_right = None

        return stance_left, stance_right
    
    def get_heigth_cm(self,tree):
        """New function to retreive height of boxer in cm. Returns None for
        values that are not included on Boxrec.com"""
        height_row = tree.xpath(
                FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "height"]/td[position() = 1 or position() = 3]'
        )

        try:
            height_left = int(
                re.findall('\d+',height_row[0].text.split('/')[1].strip())[0]
            )
        except (AttributeError, IndexError) as e:
            height_left = None

        try:
            height_right = int(
                re.findall('\d+',height_row[1].text.split('/')[1].strip())[0]
            )
        except (AttributeError, IndexError) as e:
            height_right = None

        return height_left, height_right
        
    def get_reach_cm(self,tree):
        """New function to retreive reach of boxer in cm. Returns None for
        values that are not included on Boxrec.com"""
        reach_row = tree.xpath(
                FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "reach"]/td[position() = 1 or position() =3]'
        )
        try:
            reach_left = int(
                re.findall('\d+',reach_row[0].text.split('/')[1].strip())[0]
            )
        except (AttributeError, IndexError) as e:
            reach_left = None

        try:
            reach_right = int(
                re.findall('\d+',reach_row[1].text.split('/')[1].strip())[0]
            )
        except (AttributeError, IndexError) as e:
            reach_right = None
        
        return reach_left, reach_right
    
    def get_record(self,tree):
        """New function to retreive record of boxer in cm.
        Output is a tuple with (win,loss,draw) for each boxer."""
        win_row = tree.xpath(
                FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "won"]/td[position() = 1 or position() = 3]'
        )
        win_left = self.extract_alphanumeric(win_row[0].text)
        win_right = self.extract_alphanumeric(win_row[1].text)
        lose_row = tree.xpath(
                FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "lost"]/td[position() = 1 or position() = 3]'
        )
        lose_left = self.extract_alphanumeric(lose_row[0].text)
        lose_right = self.extract_alphanumeric(lose_row[1].text)
        drawn_row = tree.xpath(
                FightParser.BASE_DOM_PATH + \
                '[./td/b/text() = "drawn"]/td[position() = 1 or position() = 3]'
        )
        drawn_left = self.extract_alphanumeric(drawn_row[0].text)
        drawn_right = self.extract_alphanumeric(drawn_row[1].text)
        
        return (win_left, lose_left, drawn_left), (win_right, lose_right, drawn_right)

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
        age_left, age_right = self.get_age(tree)
        stance_left, stance_right = self.get_stance(tree)
        height_left, height_right = self.get_heigth_cm(tree)
        reach_left, reach_right = self.get_reach_cm(tree)
        wld_left, wld_right = self.get_record(tree)
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
            age_left=age_left,
            age_right=age_right,
            stance_left=stance_left,
            stance_right=stance_right,
            height_left=height_left,
            height_right=height_right,
            reach_left=reach_left,
            reach_right=reach_right,
            record_left=wld_left,
            record_right=wld_right,
            winner=result
        )


class FightListParser(BaseParser):
    BASE_DOM_PATH = \
        '//div[@class="content"]//table[@class="calendarTable"]'

    def get_event_and_fight_ids(self, tree):
        links = tree.xpath(
            FightListParser.BASE_DOM_PATH \
                + '//td[@class="actionCell"]/div[@class="desktop"]/a[1]/@href'
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
