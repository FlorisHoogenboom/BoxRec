from . import BASE_URL
from .parsers import FailedToParse
import threading


class BaseDao(object):
    def __init__(self, session, parser):
        self.session = session
        self.parser = parser

    def parse(self, response):
        return self.parser.parse(response)


class FightDao(BaseDao):
    ENDPOINT = '/event/{event_id}/{fight_id}'
    DATE_ENDPOINT = '/date'

    def __init__(self, session, parser, fight_list_parser):
        super(FightDao, self).__init__(session, parser)
        self.fight_list_parser = fight_list_parser

    def find_by_id(self, event_id, fight_id):
        url = BASE_URL + FightDao.ENDPOINT.format(event_id=event_id, fight_id=fight_id)

        return self.parse(
            self.session.get(url)
        )

    def find_by_list(self, ids_list, soft_fail=True, multithreaded=True):
        assert ((soft_fail and multithreaded) or not multithreaded), \
            "Errors cannot bubble when using multithreading."


        fights = []
        # Closure to spawn in threads. We can safely run this
        # function in multiple threads since threads are
        # thread safe in Python.
        def find_fight_and_append(event_id, fight_id):
            try:
                fights.append(
                    self.find_by_id(event_id, fight_id)
                )
            except FailedToParse as e:
                if soft_fail:
                    fights.append(e)
                else:
                    raise e

        if multithreaded:
            threads = []

            # Create a thread to fetch the data of each fight.
            for event_id, fight_id in ids_list:
                thread = threading.Thread(
                    target=find_fight_and_append,
                    args=(event_id, fight_id),
                    name="Fetch data for event {0} and fight {1}".format(event_id, fight_id)
                )
                thread.start()
                threads.append(thread)

            # Wait for all threads to finish before
            # fetching other data.
            for thread in threads:
                thread.join()

        else:
            for event_id, fight_id in ids_list:
                find_fight_and_append(event_id, fight_id)

        return fights

    def find_by_date(self, date, soft_fail=True, multithreaded=True):
        url = BASE_URL + FightDao.DATE_ENDPOINT

        response = self.session.get(
            url,
            params={'date': date}
        )

        ids = self.fight_list_parser.parse(response)

        return self.find_by_list(
            ids, soft_fail=soft_fail, multithreaded=multithreaded
        )


class BoxerDao(BaseDao):
    ENDPOINT = '/boxer/{id}'

    def find_by_id(self, id):
        url = BASE_URL + BoxerDao.ENDPOINT.format(id=id)
        return self.parse(
            self.session.get(url)
        )