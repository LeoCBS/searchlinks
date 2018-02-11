# -*- coding: utf-8 -*-
import unittest
import os

from searchlinks.spiders.duckduckgo import DuckduckgoSpider
from searchlinks.spiders import parser
from tests import load_file


class ParserTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.current_dir = os.getcwd()
        self.spider = DuckduckgoSpider()

    def test_should_parser_item_from_response(self):
        links = parser.get_links(
            load_file('tests/resources/results.html')
        )
        self.assertEqual(len(links), 30)


if __name__ == '__main__':
    unittest.main()
