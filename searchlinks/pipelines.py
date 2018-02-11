# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import sqlite3


class SearchlinksPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    collection_name = 'duckduckgo'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class SQLiteStorePipeline(object):
    filename = '/home/leonardo/Documents/searchlinks/searchlinks'

    def process_item(self, item, spider):
        try:
            self.conn.execute('insert into proxyurls (url) values (?)',
                              (item['url'],))
            self.conn.commit()
        except sqlite3.Error as e:
            spider.logger.info('Failed to insert item {}'.format(e.args[0]))
        return item

    def open_spider(self, spider):
        try:
            self.conn = sqlite3.connect(self.filename)
        except:
            spider.logger.info('error connect to sqlite')

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
