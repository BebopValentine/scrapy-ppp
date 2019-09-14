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

    # 基本数据
    title = scrapy.Field()
    uptime = scrapy.Field()
    des = scrapy.Field()
    category = scrapy.Field()
    status = scrapy.Field()
    wordCount = scrapy.Field()

    # 小说图片
    image = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()

    # 详情
    more_des = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_content = scrapy.Field()
