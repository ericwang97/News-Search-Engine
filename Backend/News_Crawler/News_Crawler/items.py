# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class News_CrawlerItem(scrapy.Item):

    # title
    title = scrapy.Field()
    # keyword
    keyword = scrapy.Field()
    # abstract
    digest = scrapy.Field()
    # URL
    url = scrapy.Field()
    # ent_time
    ent_time = scrapy.Field()
    # content
    content = scrapy.Field()
    # comment number
    hot_degree = scrapy.Field()
    # net_name
    net_name = scrapy.Field()
    # scan_id
    scan_id = scrapy.Field()

    pass
