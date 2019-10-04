# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import datetime
from scrapy.http import Request
import requests
from bs4 import BeautifulSoup

from setu.items import IpPool

from ..libs.emailSend import EmailSend


class IpPoolSpider(scrapy.Spider):
    name = 'ip_pool'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/wt/']

    def __init__(self):
        self.max_page = ''
        self.base_url = 'https://www.xicidaili.com/wt/'

    def parse(self, response):
        """ email = EmailSend()
        content = '爬虫启动时间：{}'.format(datetime.now())
        email.send_text_email('shroudfzj@163.com',
                              '524061832@qq.com', '爬虫启动', content) """

        page = BeautifulSoup(response.text, 'lxml')
        self.max_page = page.find(
            'div', class_='pagination').find_all('a')[-2].string
        for num in range(1, 2):
            next_page = self.base_url + str(num) + '/'
            yield Request(next_page, callback=self.parse_ip)

    def parse_ip(self, response):

        ip_container = BeautifulSoup(response.text, 'lxml')
        ips = ip_container.find_all('tr', class_='odd')
        ipPoolItem = IpPool()

        for current_ip in ips:
            item = current_ip.find_all('td')
            ip = item[1].string
            port = item[2].string
            server = item[3].a.string
            theType = item[5].string
            url = theType + '://' + ip + ':' + port

            response = requests.get('http://www.baidu.com/',
                                    proxies={theType: url})

            if response.status_code == 200:
                """ print(ip)
                print(port)
                print(server)
                print(theType)
                print('-'*20) """

                ipPoolItem['ip'] = ip
                ipPoolItem['port'] = port
                ipPoolItem['theType'] = theType
                ipPoolItem['server'] = server

            yield ipPoolItem
