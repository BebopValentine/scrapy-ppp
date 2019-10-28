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


class IpPool(scrapy.Item):

    # 代理池
    ip = scrapy.Field()
    port = scrapy.Field()
    theType = scrapy.Field()
    server = scrapy.Field()


class ChengduTenancy(scrapy.Item):

    # 成都租房信息
    title = scrapy.Field()  # 信息名
    price = scrapy.Field()  # 价格
    curLongitude = scrapy.Field()  # 经度
    curLatitude = scrapy.Field()  # 纬度
    house = scrapy.Field()  # 出租方式
    typ = scrapy.Field()  # 房屋类型
    area = scrapy.Field()  # 面积
    orient = scrapy.Field()  # 朝向
    publishTime = scrapy.Field()  # 发布时间
    liveTime = scrapy.Field()  # 入住
    tenancy = scrapy.Field()  # 租期
    checkRoom = scrapy.Field()  # 看房
    storey = scrapy.Field()  # 楼层
    elevator = scrapy.Field()  # 电梯
    parking = scrapy.Field()  # 车位
    water = scrapy.Field()  # 用水
    electricity = scrapy.Field()  # 用电
    gas = scrapy.Field()  # 燃气
