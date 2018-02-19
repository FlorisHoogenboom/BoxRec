import requests
from .data_access import BoxerDao, FightDao
from .parsers import BoxerParser, FightParser


class FightService(object):
    def __init__(
        self, session, fight_parser, boxer_parser
    ):
        self.fight_dao = FightDao(
            session,
            fight_parser
        )

        self.boxer_dao = BoxerDao(
            session,
            boxer_parser
        )

    def find_by_id(self, event_id, fight_id):
        fight = self.fight_dao.find_by_id(event_id, fight_id)

        fight.boxer_left = self.boxer_dao.find_by_id(
            fight.boxer_left_id
        )

        fight.boxer_right = self.boxer_dao.find_by_id(
            fight.boxer_right_id
        )

        return fight

class FightServiceFactory(object):
    @staticmethod
    def make_service(session=None):
        if session is None:
            session = requests.session()

        return FightService(
            session, FightParser(), BoxerParser()
        )
