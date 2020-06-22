# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from News_Crawler import settings
import logging
import time

class News_CrawlerPipeline(object):
    source_urlselect = '''select url from {}'''.format(settings.TABLE_NAME)
    url_list = []

    scrapyInsert = '''insert into {}(title,url,net_name,ent_time,keyword,digest,content,hot_degree,scan_id)
                            values('{title}','{url}','{net_name}','{ent_time}','{keyword}','{digest}','{content}','{hot_degree}','{scan_id}')'''

    source_scanInsert = '''insert into netfin_scanlog(id,net_name,status,ent_time,fail_result)
                                        values('{scan_id}','{net_name}','{status}','{ent_time}','{fail_result}')'''


    def __init__(self):
        # Connect to MySQL
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            port=settings.MYSQL_PORT,
            charset='utf8',
            use_unicode=True)


        # Use cursor to upsert
        self.cursor = self.connect.cursor()
        print('MySQL is successfully connected')
        self.connect.autocommit(True)

        # get the URLs from database
        self.cursor.execute(self.source_urlselect)
        for r in self.cursor:
            self.url_list.append(r[0])

    def process_item(self, item, spider):
        try:
            if item['url'] in self.url_list:
                print('URL is already existed')
                return

            else:
                print('You find a related article! Start inserting in MySQL')

                sqltext = self.scrapyInsert.format(
                    settings.TABLE_NAME,
                    title=pymysql.escape_string(item['title']),
                    url=pymysql.escape_string(item['url']),
                    net_name=pymysql.escape_string(item['net_name']),
                    ent_time=pymysql.escape_string(item['ent_time']),
                    keyword=pymysql.escape_string(item['keyword']),
                    digest=pymysql.escape_string(item['digest']),
                    content=pymysql.escape_string(item['content']),
                    hot_degree=pymysql.escape_string(item['hot_degree']),
                    scan_id = pymysql.escape_string(item['scan_id']))
                self.cursor.execute(sqltext)
                print('MySQL successfully inserts the data')
                self.connect.commit()

        except Exception as error:
            logging.log(error)

        return item

    def open_spider(self, spider):
        sqltext = self.source_scanInsert.format(scan_id=pymysql.escape_string(spider.scan_id),
                                                net_name=pymysql.escape_string('Tencent.scrapy'),
                                                status=pymysql.escape_string('1'),
                                                ent_time=pymysql.escape_string(
                                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))),
                                                fail_result=pymysql.escape_string('started')
                                                )
        # spider.log(sqltext)
        self.cursor.execute(sqltext)
        print('MySQL successfully inserts the START log')

    def close_spider(self, spider):
        sqltext = self.source_scanInsert.format(scan_id=pymysql.escape_string(spider.scan_id),
                                                net_name=pymysql.escape_string('Tencent.scrapy'),
                                                status=pymysql.escape_string('2'),
                                                ent_time=pymysql.escape_string(
                                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))),
                                                fail_result=pymysql.escape_string('finished')
                                                )
        self.cursor.execute(sqltext)
        print('MySQL is disconnected')
        self.cursor.close()
        self.connect.close()

