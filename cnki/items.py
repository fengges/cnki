# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CnkiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CnkiPassItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # can you see hehe
    pass

class CnkiListPassItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url=scrapy.Field()

    pass