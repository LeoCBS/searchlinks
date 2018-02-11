# -*- coding: utf-8 -*-
import scrapy
import time

from searchlinks.spiders import parser

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

MAX_PAGES = 5


def write_response_body(body):
    name = "{}.html".format(time.time())
    with open(name, 'a') as the_file:
        the_file.write(body)


class DuckduckgoSpider(scrapy.Spider):
    name = 'duckduckgo'
    start_url = "https://duckduckgo.com/html/"
    body_tmp = "q={}&b=&kl=us-en"
    start_index = 30
    body_nextpage_tmp = "q={}&s={}&nextParams=&v=l&o=json&dc=25&api=%2Fd.js&kl=us-en"

    def start_requests(self):
        self.pages_count = 0
        q = getattr(self, 'q', None)
        body = self.body_tmp.format(q)
        yield scrapy.Request(
            method="POST",
            headers=headers,
            body=body,
            url=self.start_url,
            meta={'q': q},
            callback=self.parse)

    def parse(self, response):
        write_response_body(response.body.decode())
        self.pages_count += 1
        links = parser.get_links(response.body)
        for l in links:
            yield {'url': l}
        q = response.meta['q']
        body = self.body_nextpage_tmp.format(q, self.start_index)
        self.start_index += 50
        if self.pages_count < MAX_PAGES:
            yield scrapy.Request(
                method="POST",
                headers=headers,
                body=body,
                url=self.start_url,
                meta={'q': q},
                callback=self.parse)
