# -*- coding: utf-8 -*-
import scrapy
from setu.items import BookInfo
import bs4
from bs4 import BeautifulSoup
from scrapy.http import Request


class BookInfoSpider(scrapy.Spider):
    name = 'book_info'
    allowed_domains = ['x23qb.com']
    start_urls = ['http://x23qb.com/lightnovel/1/']

    def __init__(self):
        self.base_url = 'https://www.x23qb.com/lightnovel/'

    def parse(self, response):
        # 获取到各页面的连接

        current_page = BeautifulSoup(response.text, 'lxml')
        current_page_num = current_page.find(
            'div', class_='pagelink').span.string.split('/')[0]

        # * 为测试不放开页面限制
        for item in range(1, 2):
            next_page = self.base_url + str(item) + '/'
            yield Request(next_page, callback=self.parse_page)

    def parse_page(self, response):
        p_current_page = BeautifulSoup(response.text, 'lxml')
        books_box = p_current_page.find('div', id="sitebox").find_all('dl')
        book_info = BookInfo()
        for book in books_box:
            if type(book) is not bs4.element.NavigableString:
                book_category = book.find('span').string

                # 排除半吊子作者写的网文
                if book_category != '轻小说の' and book_category != '轻の小说':
                    book_info['book_id'] = book.a['href'].split('/')[-2]
                    book_info['book_name'] = book.a.img['alt']
                    book_info['book_simple_des'] = book.find_all(
                        'dd', class_='book_des')[0].string
                    book_info['book_category'] = book_category
                    book_info['book_word_count'] = book.find_all('dd', class_='book_other')[
                        0].find_all('span')[-1].string
                    book_info['image_url'] = book.a.img['_src']
                    yield book_info
