from .config import BASE_URL


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

    def find_by_date(self, date):
        url = BASE_URL + FightDao.DATE_ENDPOINT

        response = self.session.get(
            url,
            params={'date': date}
        )

        ids = self.fight_list_parser.parse(response)

        fights = [
            self.find_by_id(event_id, fight_id) for event_id, fight_id in ids
        ]

        return fights


class BoxerDao(BaseDao):
    ENDPOINT = '/boxer/{id}'

    def find_by_id(self, id):
        url = BASE_URL + BoxerDao.ENDPOINT.format(id=id)
        return self.parse(
            self.session.get(url)
        )