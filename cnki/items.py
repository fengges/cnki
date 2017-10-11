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
    num=scrapy.Field()
    pass

class CnkiKeyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # HHHHHHHH TEST
    word=scrapy.Field()
    page=scrapy.Field()
    allpage=scrapy.Field()
    pass
class CnkiCiteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    citeId = scrapy.Field()
    citeUrl = scrapy.Field()
    type=scrapy.Field()
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

#abstract Item
class CnkiAbstractItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # HHHHHHHH TEST
    id = scrapy.Field()
    author=scrapy.Field()
    organization=scrapy.Field()
    abstract=scrapy.Field()
    fund=scrapy.Field()
    pass