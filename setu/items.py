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


class BookInfo(scrapy.Item):

    # 基本信息
    book_id = scrapy.Field()
    book_name = scrapy.Field()
    book_simple_des = scrapy.Field()
    book_category = scrapy.Field()
    book_word_count = scrapy.Field()

    # 封面
    image_url = scrapy.Field()


class BookChapters(scrapy.Item):

    # 章节
    book_id = scrapy.Field()
    book_name = scrapy.Field()
    chapter_info = scrapy.Field()
