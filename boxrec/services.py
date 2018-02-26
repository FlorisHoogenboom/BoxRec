import requests
import lazy_object_proxy
from .data_access import BoxerDao, FightDao
from .parsers import (
    BoxerParser, FightParser,
    FightListParser
)


class FightService(object):
    """Service class that allows access to BoxRec

    This class provides access to the data presented on
    BoxRec by a simple API.
    """
    def __init__(self, fight_dao, boxer_dao):
        """
        :param fight_dao: The Data Access Object that should be used for Fights
        :param boxer_dao: The Data Access Object that should be used for Boxers
        """
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
        """
        Method to query all information of a specific Fight by it's id.
        :param event_id: (int or str) The id of the event
        :param fight_id: (int or str) The id of the fight
        :param lazy_load: (bool, default=True) Initialize related data lazily
        :return: (Fight) Fight Object will all the fight's information.
        """
        fight = self.fight_dao.find_by_id(event_id, fight_id)

        if lazy_load:
            return self._add_boxers_to_fight_lazy(fight)
        else:
            return self._add_boxers_to_fight(fight)

    def find_by_url(self, url):
        """
        Method to query all information of a specific fight by its URL.
        :param url: The URL of a fight on BoxRec
        :return: (Fight) Fight Object will all the fight's information.
        """
        event_id = url.rsplit('/')[-2]
        fight_id = url.rsplit('/')[-1]
        return self.find_by_id(event_id, fight_id)

    def find_by_date(self, date, lazy_load=True, soft_fail=True):
        """
        Method to get all fights for a specific date.
        :param date: (str) Date in the format (yyyy-mm-dd)
        :param lazy_load: (bool, default=True) Whether to intialize relations lazily
        :return: (list) A list of Fight objects.
        """
        fights_list = self.fight_dao.find_by_date(date, soft_fail=soft_fail)

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
    """Factory class for initializing the FightService
    """
    @staticmethod
    def make_service(session=None):
        """
        Static method that builds the FightService
        :param session: (requests.Session) A session instance of Requests
        :return: (FightService) An instance of the FightService using the specified session.
        """
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
