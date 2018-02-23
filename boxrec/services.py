import requests
import lazy_object_proxy
from .data_access import BoxerDao, FightDao
from .parsers import (
    BoxerParser, FightParser,
    FightListParser
)


class FightService(object):
    def __init__(self, fight_dao, boxer_dao):
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

    def _add_boxers_to_fight_lazy(self, fight):
        """
        Method for initializing boxers as proxy objects that
        only load data when called.
        :param fight: (Fight) instance of Fight for which to load the boxers
        :return: The same instance of Fight with the boxers added as Proxies
        """
        fight.boxer_left = lazy_object_proxy.Proxy(
            lambda: self.boxer_dao.find_by_id(fight.boxer_left_id)
        )

        fight.boxer_right = lazy_object_proxy.Proxy(
            lambda: self.boxer_dao.find_by_id(fight.boxer_right_id)
        )

        return fight

    def find_by_id(self, event_id, fight_id, lazy_load=True):
        fight = self.fight_dao.find_by_id(event_id, fight_id)

        if lazy_load:
            return self._add_boxers_to_fight_lazy(fight)
        else:
            return self._add_boxers_to_fight(fight)

    def find_by_url(self, url):
        event_id = url.rsplit('/')[-2]
        fight_id = url.rsplit('/')[-1]
        return self.find_by_id(event_id, fight_id)

    def find_by_date(self, date, lazy_load=True):
        fights_list = self.fight_dao.find_by_date(date)

        if lazy_load:
            fights_with_boxers = map(
                self._add_boxers_to_fight_lazy,
                fights_list
            )
        else:
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
