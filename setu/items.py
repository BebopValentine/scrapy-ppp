# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SetuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LightItem(scrapy.Item):

    # 封面数据
    title = scrapy.Field()
    uptime = scrapy.Field()
    des = scrapy.Field()
    category = scrapy.Field()
    status = scrapy.Field()
    wordCount = scrapy.Field()
