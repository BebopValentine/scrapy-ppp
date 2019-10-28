# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import requests
from bs4 import BeautifulSoup
import re

from setu.items import ChengduTenancy


class CdzfSpider(scrapy.Spider):
    name = 'cdzf'
    allowed_domains = ['cd.lianjia.com']
    start_urls = ['https://cd.lianjia.com/zufang/']

    def __init__(self):
        self.base_url = 'https://cd.lianjia.com'
        self.max_page = ''

    def parse(self, response):
        page_content = BeautifulSoup(response.text, 'lxml')
        page_navi = page_content.find('div', class_='content__pg')

        self.max_page = page_navi['data-totalpage']

        for page_num in range(1, int(self.max_page)):
            page_url = self.base_url + '/zufang/pg' + str(page_num)
            yield Request(page_url, callback=self.parse_page)

    def parse_page(self, response):
        list_page = BeautifulSoup(response.text, 'lxml')
        list_container = list_page.find('div', class_='content__list')
        list_item = list_container.find_all(
            'div', class_='content__list--item')
        for item in list_item:
            item_detail_url = self.base_url + item.find_all(
                'a', class_='content__list--item--aside')[0]['href']
            # 独栋公寓与其他房源的 html 结构不一样
            tag = item.find_all(
                'i', class_='content__item__tag--authorization_apartment')
            if tag and len(tag) == 1:
                # 独栋公寓
                yield
                # yield Request(item_detail_url, callback=self.parse_apartment_detail)
            else:
                # 普通房源
                yield Request(item_detail_url, callback=self.parse_normal_detail)

    def parse_normal_detail(self, response):

        normal_detail = BeautifulSoup(response.text, 'lxml')

        title = normal_detail.find('p', class_='content__title').string
        price = normal_detail.find(
            'p', class_='content__aside--title').find('span').string
        pre_cur = normal_detail.find_all('script')[5]
        cur_latitude = re.findall(re.compile(
            "latitude:\s*'(\d+)\.(\d+)'"), str(pre_cur))
        cur_longitude = re.findall(re.compile(
            "longitude:\s*'(\d+)\.(\d+)'"), str(pre_cur))
        main_info = normal_detail.find('p', class_='content__article__table')
        base_info = normal_detail.find_all('li', class_='fl oneline')

        chengdu = ChengduTenancy()

        chengdu['title'] = title  # 信息名
        chengdu['price'] = price  # 价格
        chengdu['curLongitude'] = cur_longitude[0][0] + \
            '.' + cur_longitude[0][1]  # 经度
        chengdu['curLatitude'] = cur_latitude[0][0] + \
            '.' + cur_latitude[0][1]  # 纬度
        chengdu['house'] = main_info.find_all('span')[0].contents[1]  # 出租方式
        chengdu['typ'] = main_info.find_all('span')[1].contents[1]  # 房屋类型
        chengdu['area'] = main_info.find_all('span')[2].contents[1]  # 面积
        chengdu['orient'] = main_info.find_all('span')[3].contents[1]  # 朝向
        chengdu['publishTime'] = base_info[1].string.split('：')[1]  # 发布时间
        chengdu['liveTime'] = base_info[2].string.split('：')[1]  # 入住
        chengdu['tenancy'] = base_info[4].string.split('：')[1]  # 租期
        chengdu['checkRoom'] = base_info[5].string.split('：')[1]  # 看房
        chengdu['storey'] = base_info[7].string.split('：')[1]  # 楼层
        chengdu['elevator'] = base_info[8].string.split('：')[1]  # 电梯
        chengdu['parking'] = base_info[10].string.split('：')[1]  # 车位
        chengdu['water'] = base_info[11].string.split('：')[1]  # 用水
        chengdu['electricity'] = base_info[13].string.split('：')[1]  # 用电
        chengdu['gas'] = base_info[14].string.split('：')[1]  # 燃气

        print(title)
        print(price)
        print(cur_longitude[0][0] + '.' + cur_longitude[0][1])
        print(cur_latitude[0][0] + '.' + cur_latitude[0][1])

        print(main_info.find_all('span')[0].contents[1])
        print(main_info.find_all('span')[1].contents[1])
        print(main_info.find_all('span')[2].contents[1])
        print(main_info.find_all('span')[3].contents[1])

        print(base_info[1].string.split('：')[1])
        print(base_info[2].string.split('：')[1])
        print(base_info[4].string.split('：')[1])
        print(base_info[5].string.split('：')[1])
        print(base_info[7].string.split('：')[1])
        print(base_info[8].string.split('：')[1])
        print(base_info[10].string.split('：')[1])
        print(base_info[11].string.split('：')[1])
        print(base_info[13].string.split('：')[1])
        print(base_info[14].string.split('：')[1])
        print('='*30)

        yield chengdu
