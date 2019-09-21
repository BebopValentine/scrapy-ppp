# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from setu.items import BookInfo, BookChapters, BookContents


class SetuPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if isinstance(item, BookInfo):
            # 处理书籍
            self.db['books'].insert(dict(item))
            return item
        elif isinstance(item, BookChapters):
            # 处理章节
            self.db['chapters'].insert(dict(item))
            return item
        elif isinstance(item, BookContents):
            # 处理章节
            self.db['contents'].insert(dict(item))
            return item

    def close_spider(self, spider):
        self.client.close()
