# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CnkiKeyWordItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # HHHHHHHH TEST
    word=scrapy.Field()
    pass

class CnkiPassItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    pass

class CnkiListPassItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url=scrapy.Field()
    pubdata=scrapy.Field()
    cite=scrapy.Field()
    citeUrl=scrapy.Field()
    download=scrapy.Field()
    source=scrapy.Field()
    type=scrapy.Field()
    pass