import requests
from .data_access import BoxerDao, FightDao
from .parsers import (
    BoxerParser, FightParser,
    FightListParser
)


class FightService(object):
    def __init__(
        self, session, fight_parser,
        fight_list_parser, boxer_parser
    ):
        self.fight_dao = FightDao(
            session,
            fight_parser,
            fight_list_parser
        )

        self.boxer_dao = BoxerDao(
            session,
            boxer_parser
        )

    def _add_boxers_to_fight(self, fight):
        fight.boxer_left = self.boxer_dao.find_by_id(
            fight.boxer_left_id
        )

        fight.boxer_right = self.boxer_dao.find_by_id(
            fight.boxer_right_id
        )

        return fight

    def find_by_id(self, event_id, fight_id):
        fight = self.fight_dao.find_by_id(event_id, fight_id)
        fight_with_boxers = self._add_boxers_to_fight(fight)

        return fight_with_boxers

    def find_by_url(self, url):
        event_id = url.rsplit('/')[-2]
        fight_id = url.rsplit('/')[-1]
        return self.find_by_id(event_id, fight_id)

    def find_by_date(self, date):
        fights_list = self.fight_dao.find_by_date(date)

        fights_with_boxers = map(
            self._add_boxers_to_fight,
            fights_list
        )

        return list(fights_with_boxers)


class FightServiceFactory(object):
    @staticmethod
    def make_service(session=None):
        if session is None:
            session = requests.session()

        return FightService(
            session, FightParser(),
            FightListParser(), BoxerParser()
        )
