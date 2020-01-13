# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import datetime
import bs4
from bs4 import BeautifulSoup
from scrapy.http import Request

from setu.items import BookInfo
from setu.items import BookChapters
from setu.items import BookContents

from ..libs.emailSend import EmailSend


class BookChaptersSpider(scrapy.Spider):
    name = 'light_novel'
    allowed_domains = ['x23qb.com']
    start_urls = ['http://x23qb.com/lightnovel/1/']

    def __init__(self):
        self.base_url = 'https://www.x23qb.com/lightnovel/'
        self.content_base_url = 'https://www.x23qb.com/'
        self.chapter_content = []

    def parse(self, response):
        # 获取各页面链接
        """ email = EmailSend()
        content = '爬虫启动时间：{}'.format(datetime.now())
        email.send_text_email('shroudfzj@163.com',
                              '524061832@qq.com', '爬虫启动', content) """

        current_page = BeautifulSoup(response.text, 'lxml')
        current_page_num = current_page.find(
            'div', class_='pagelink').span.string.split('/')[1]

        print('-------------'+current_page_num)

        # * 为测试不放开页面限制
        for item in range(1, int(current_page_num)):
            next_page = self.base_url + str(item) + '/'
            yield Request(next_page, callback=self.parse_page)

    def parse_page(self, response):
        # 获取书籍基本信息
        book_info = BookInfo()

        current_books = BeautifulSoup(response.text, 'lxml')
        books = current_books.find('div', id="sitebox").find_all('dl')
        for book in books:
            if type(book) is not bs4.element.NavigableString:
                book_category = book.find('span').string

                # 排除网文
                # 写入书籍基本信息
                if book_category != '轻小说の' and book_category != '轻の小说':
                    book_info['bookId'] = book.a['href'].split('/')[-2]
                    book_info['bookName'] = book.a.img['alt']
                    book_info['bookSimpleDes'] = book.find_all(
                        'dd', class_='book_des')[0].string
                    book_info['bookCategory'] = book_category
                    book_info['bookWordCount'] = book.find_all('dd', class_='book_other')[
                        0].find_all('span')[-1].string
                    book_info['imageUrl'] = book.a.img['_src']
                    current_book = book.dt.a['href']
                    yield book_info
                    yield Request(current_book, callback=self.parse_book)

    def parse_book(self, response):

        # 解析章节标题
        book_chapter = BookChapters()
        book_contents = BookContents()

        current_book = BeautifulSoup(response.text, 'lxml')
        book_contents['bookId'] = current_book.find(
            'div', id='bookimg').img['src'].split('/')[-2]
        book_contents['bookName'] = current_book.find(
            'div', class_='d_title').h1.string

        boks_list = []
        the_list = current_book.find('ul', id='chapterList').find_all('a')
        for bok in the_list:
            info = {}
            info['chapter_name'] = bok.string
            info['chapter_id'] = bok['href'].split('/')[-1].split('.')[-2]
            boks_list.append(info)

        book_chapter['bookName'] = current_book.find(
            'div', class_='d_title').h1.string
        book_chapter['bookId'] = current_book.find('img')['src'].split('/')[-2]
        book_chapter['chapterInfo'] = boks_list

        rawIntro = current_book.find('div', id='bookintro').p.contents
        cookedIntro = []
        for item in rawIntro:
            sentence = ''
            if type(item) is bs4.element.Tag:
                pass
            elif item[:1] == '\n':
                sentence = item[1:]
            else:
                sentence = item
            if sentence != '':
                cookedIntro.append(sentence)
        book_chapter['bookIntro'] = ''.join(cookedIntro)

        for chapter in the_list:
            current_contents = self.content_base_url + chapter['href'][1:]
            chapterId = chapter['href'].split('/')[-1].split('.')[-2]
            chapterName = chapter.string
            yield Request(current_contents, meta={'bookContents': book_contents, 'chapterId': chapterId, 'chapterName': chapterName, 'alreadyContent': []}, callback=self.parse_content)
        yield book_chapter

    def parse_content(self, response):

        # 解析章节内容

        contents = BeautifulSoup(response.text, 'lxml')
        book_content = response.meta['bookContents']
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
            print("组合出的文章下一页地址："+next_page)
            yield Request(next_page, meta={'bookContents': book_content, 'chapterId': chapterId, 'chapterName': chapterName, 'alreadyContent': container}, callback=self.parse_content)

        book_content['chapterContent'] = container
        book_content['chapterId'] = response.meta['chapterId']
        book_content['chapterName'] = response.meta['chapterName']
        yield book_content


"""     def closed(self, reason):
        # 爬虫关闭的时候，会调用这个方法
        email = EmailSend()
        content = '爬虫关闭时间：{}'.format(datetime.now())
        email.send_text_email('shroudfzj@163.com',
                              '524061832@qq.com', '爬虫结束', content) """
