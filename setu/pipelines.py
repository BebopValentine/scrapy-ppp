# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from setu.items import BookInfo, BookChapters, BookContents, IpPool, ChengduTenancy

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


class SetuPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

        self.host_server = 'smtp.163.com'
        self.sender_qq = 'shroudfzj@163.com'
        self.pwd = 'fzjinspur0203'
        self.sender_qq_mail = 'shroudfzj@163.com'
        self.receiver = '524061832@qq.com'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.send_mail('爬虫开始工作')

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if isinstance(item, BookInfo):
            # 处理书籍
            collection = self.db['books']
            condition = {'bookName': item['bookName']}

            queryRes = collection.find_one(condition)
            if queryRes:
                collection.update(condition, dict(item))
            else:
                collection.insert(dict(item))
            return item
        elif isinstance(item, BookChapters):
            # 处理章节
            collection = self.db['chapters']
            condition = {'bookName': item['bookName']}

            queryRes = collection.find_one(condition)
            if queryRes:
                collection.update(condition, dict(item))
            else:
                collection.insert(dict(item))
            return item

        elif isinstance(item, BookContents):
            # 处理章节
            collection = self.db['contents']
            condition = {
                'chapterName': item['chapterName'], 'bookName': item['bookName']}

            queryRes = collection.find_one(condition)
            if queryRes:
                collection.update(condition, dict(item))
            else:
                collection.insert(dict(item))
            return item

        elif isinstance(item, IpPool):
            # 代理池
            collection = self.db['ips']
            condition = {'ip': item['ip']}

            queryRes = collection.find_one(condition)
            if queryRes:
                collection.update(condition, dict(item))
            else:
                collection.insert(dict(item))
            return item

        elif isinstance(item, ChengduTenancy):
            # 代理池
            collection = self.db['cdzf']
            condition = {'title': item['title']}

            queryRes = collection.find_one(condition)
            if queryRes:
                collection.update(condition, dict(item))
            else:
                collection.insert(dict(item))
            return item

    def close_spider(self, spider):
        self.send_mail('爬虫结束工作')

        self.client.close()

    def send_mail(self, title):
        # 邮件的正文内容
        mail_content = '你好，爬虫结束工作'
        # 邮件标题
        mail_title = title

        smtp = SMTP_SSL(self.host_server)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(1)
        smtp.ehlo(self.host_server)
        smtp.login(self.sender_qq, self.pwd)

        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = self.sender_qq_mail
        msg["To"] = self.receiver
        smtp.sendmail(self.sender_qq_mail, self.receiver, msg.as_string())
        smtp.quit()
