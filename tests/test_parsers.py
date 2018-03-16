import unittest
from boxrec.parsers import FightParser


class MockResponse(object):
    def __init__(self, content, encoding, url):
        self.content= content
        self.encoding = encoding
        self.url = url


class TestFightParser(unittest.TestCase):
    def setUp(self):
        with open('mock_data/fights/draw.html', 'rb') as file:
            self.drawn_fight = file.read()

        self.parser = FightParser()

    def test_parses_draw(self):
        """Test it correctly handles draws"""
        mock_response = MockResponse(
            self.drawn_fight,
            'UTF-8',
            "http://boxrec.com/en/event/115689/202488"
        )

        result = self.parser.parse(mock_response)
        self.assertEqual(result.winner, 'drawn', "Result should equal draw.")


class TestBoxerParser(unittest.TestCase):
    pass