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
    bookId = scrapy.Field()
    bookName = scrapy.Field()
    bookSimpleDes = scrapy.Field()
    bookCategory = scrapy.Field()
    bookWordCount = scrapy.Field()

    # 封面
    imageUrl = scrapy.Field()


class BookChapters(scrapy.Item):

    # 章节
    bookId = scrapy.Field()
    bookName = scrapy.Field()
    bookIntro = scrapy.Field()
    chapterInfo = scrapy.Field()


class BookContents(scrapy.Item):

    # 章节
    bookId = scrapy.Field()
    bookName = scrapy.Field()
    chapterId = scrapy.Field()
    chapterName = scrapy.Field()
    chapterContent = scrapy.Field()
