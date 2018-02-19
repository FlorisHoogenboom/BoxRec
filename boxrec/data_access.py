from . import BASE_URL


class BaseDao(object):
    def __init__(self, session, parser):
        self.session = session
        self.parser = parser

    def parse(self, response):
        return self.parser.parse(response)


class FightDao(BaseDao):
    ENDPOINT = '/event/{event_id}/{fight_id}'

    def find_by_id(self, event_id, fight_id):
        url = BASE_URL + FightDao.ENDPOINT.format(event_id=event_id, fight_id=fight_id)

        return self.parse(
            self.session.get(url)
        )


class BoxerDao(BaseDao):
    ENDPOINT = '/boxer/{id}'

    def find_by_id(self, id):
        url = BASE_URL + BoxerDao.ENDPOINT.format(id=id)
        return self.parse(
            self.session.get()
        )