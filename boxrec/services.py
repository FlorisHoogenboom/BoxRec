import requests
from .data_access import BoxerDao, FightDao
from .parsers import (
    BoxerParser, FightParser,
    FightListParser
)


class FightService(object):
    def __init__(
        self, fight_dao, boxer_dao
    ):
        self.fight_dao = fight_dao
        self.boxer_dao = boxer_dao

    def _add_boxers_to_fight(self, fight):
        fight.boxer_left = self.boxer_dao.find_by_id(
            fight.boxer_left_id
        )

        fight.boxer_right = self.boxer_dao.find_by_id(
            fight.boxer_right_id
        )

        return fight

    def find_by_id(self, event_id, fight_id, recursive=False):
        fight = self.fight_dao.find_by_id(event_id, fight_id)
        if recursive:
            return self._add_boxers_to_fight(fight)
        else:
            return fight

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

        fight_dao = FightDao(
            session,
            FightParser(),
            FightListParser()
        )

        boxer_dao = BoxerDao(
            session,
            BoxerParser()
        )

        return FightService(
            fight_dao, boxer_dao
        )
