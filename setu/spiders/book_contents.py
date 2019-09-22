# -*- coding: utf-8 -*-
import scrapy
from setu.items import BookContents
import bs4
from bs4 import BeautifulSoup
from scrapy.http import Request


class BookChaptersSpider(scrapy.Spider):
    name = 'book_contents'
    allowed_domains = ['x23qb.com']
    start_urls = ['http://x23qb.com/lightnovel/1/']

    def __init__(self):
        self.base_url = 'https://www.x23qb.com/lightnovel/'
        self.content_base_url = 'https://www.x23qb.com/'
        self.chapter_content = []

    def parse(self, response):
        # 获取页面

        current_page = BeautifulSoup(response.text, 'lxml')
        current_page_num = current_page.find(
            'div', class_='pagelink').span.string.split('/')[0]

        # * 为测试不放开页面限制
        for item in range(1, 2):
            next_page = self.base_url + str(item) + '/'
            yield Request(next_page, callback=self.parse_page)

    def parse_page(self, response):

        # 获取书籍

        p_current_page = BeautifulSoup(response.text, 'lxml')
        books_box = p_current_page.find('div', id="sitebox").find_all('dl')
        for book in books_box:
            if type(book) is not bs4.element.NavigableString:
                book_category = book.find('span').string

                # 排除半吊子作者写的网文
                if book_category != '轻小说の' and book_category != '轻の小说':
                    current_book = book.dt.a['href']
                    yield Request(current_book, callback=self.parse_book)

    def parse_book(self, response):

        # 解析章节标题
        boks = BeautifulSoup(response.text, 'lxml')

        book_contents = BookContents()
        book_contents['bookId'] = boks.find(
            'div', id='bookimg').img['src'].split('/')[-2]
        book_contents['bookName'] = boks.find(
            'div', class_='d_title').h1.string

        the_list = boks.find('ul', id='chapterList').find_all('a')
        for chapter in the_list:
            current_contents = self.content_base_url + chapter['href'][1:]
            chapterId = chapter['href'].split('/')[-1].split('.')[-2]
            chapterName = chapter.string
            yield Request(current_contents, meta={'bookContents': book_contents, 'chapterId': chapterId, 'chapterName': chapterName, 'alreadyContent': []}, callback=self.parse_content)

    def parse_content(self, response):

        # 解析章节内容
        contents = BeautifulSoup(response.text, 'lxml')
        contentsItem = response.meta['bookContents']
        chapterId = response.meta['chapterId']
        chapterName = response.meta['chapterName']

        tags = contents.find_all('br')

        # 规避彩图页
        if len(tags) == 0:
            return
        container = response.meta['alreadyContent']

        for tag in tags:
            current_line = tag.previous_sibling
            if current_line != '\n' and type(current_line) is not bs4.element.Tag:
                current_line = ''.join(current_line.split())
                container.append(current_line)

        if type(tags[-1].next_sibling) is not bs4.element.Tag:
            try:
                container.append(tags[-1].next_sibling)
            except IndexError as e:
                print(response)

        # 如果有下一页则继续爬取
        if container[-1] and type(container[-1]) is not bs4.element.NavigableString:
            next_page = self.content_base_url + \
                contents.find('p', class_='mlfy_page').find_all(
                    'a')[-1]['href'][1:]
            yield Request(next_page, meta={'bookContents': contentsItem, 'chapterId': chapterId, 'chapterName': chapterName, 'alreadyContent': container}, callback=self.parse_content)

        contentsItem['chapterContent'] = container
        contentsItem['chapterId'] = response.meta['chapterId']
        contentsItem['chapterName'] = response.meta['chapterName']
        yield contentsItem
