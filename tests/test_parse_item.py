import unittest
from globocomtrends.spiders.globocom import GlobocomSpider
from globocomtrends.tests import fake_response_from_file

class GlobocomSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = GlobocomSpider()

    def test_parse(self):
        self.setUp()
        item = self.spider.parse_item(fake_response_from_file('raw_files/globo.html'))
        self.assertIsNotNone(item['title'])

if __name__ == '__main__':
    unittest.main()
