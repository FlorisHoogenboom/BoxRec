import unittest
from unittest import mock
from boxrec.data_access import BoxerDao, BASE_URL
from boxrec.models import Boxer


class MockSession(object):
    def get(self, url):
        pass

class MockBoxerParser(object):
    NAME = 'abc'
    ID = 1
    def parse(self, response):
        return Boxer(id=self.ID, name=self.NAME)


class TestBoxerDao(unittest.TestCase):
    def setUp(self):
        self.session = MockSession()
        self.parser = MockBoxerParser()

        self.dao = BoxerDao(self.session, self.parser)

    def test_calls_get_on_session(self):
        """Test if the get method of the session is called."""
        self.session.get = mock.MagicMock(return_value=None)

        self.dao.find_by_id(1)

        self.session.get.assert_called_with(
            BASE_URL + BoxerDao.ENDPOINT.format(id=1)
        )

    def test_calls_parser_with_respone(self):
        """Test the response is forwarded to the parser."""
        # Create an empty python object
        response = object()

        self.session.get = mock.MagicMock(return_value=response)
        self.parser.parse = mock.MagicMock()

        self.dao.find_by_id(123456)

        # Use comparison based on adresses to check the correct object is passed
        self.parser.parse.assert_called_with(response)

    def test_returns_parser_result(self):
        """Test if it returns the parser result."""
        return_value = self.dao.find_by_id(1234)

        self.assertIsInstance(
            return_value,
            Boxer,
            "Returned object should be instance of Boxer class."
        )

        self.assertEqual(
            return_value.name,
            MockBoxerParser.NAME
        )

        self.assertEqual(
            return_value.id,
            MockBoxerParser.ID
        )
