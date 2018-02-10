# -*- coding: utf-8 -*-
import scrapy
import csv
import sqlite3

from bs4 import BeautifulSoup

headers = {
        'Host': 'duckduckgo.com',
        'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://duckduckgo.com/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
}

input_sqlite_path = ""


def _load_inputs_sqlite(sqlitedb):
    conn = sqlite3.connect(sqlitedb)
    cur = conn.cursor()
    q = "SELECT cnpj, name FROM inputsc WHERE status = 0 LIMIT 100000"

    for r in cur.execute(q).fetchall():
        yield {'cnpj': r[0], 'name': r[1]}


def _load_inputs():
    with open('./inputs/sc0-10000.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row


class DuckduckgoSpider(scrapy.Spider):
    name = 'duckduckgo'
    start_url = "https://duckduckgo.com/html/"
    body_tmp = "q={}&b=&kl=us-en"

    def start_requests(self):
        sqlitedb = getattr(self, 'sqlitedb', None)
        inputs = _load_inputs_sqlite(sqlitedb)
        for i in inputs:
            self.logger.info("input loaded {}".format(i))
            body = self.body_tmp.format(i['name'])
            yield scrapy.Request(
                    method="POST",
                    headers=headers,
                    body=body,
                    url=self.start_url,
                    meta={'input': i},
                    callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        div_result = soup.find(
            'div',
            {'class': 'links_main links_deep result__body'}
        )
        a = div_result.find('a', {'class': 'result__url'})
        i = response.meta['input']
        yield {
                'url': a['href'],
                'name': i['name'],
                'cnpj': i['cnpj']
        }
