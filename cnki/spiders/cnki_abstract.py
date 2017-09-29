# -*- coding: utf-8 -*-
import scrapy
import codecs
import urllib
import time
import re
import json

from scrapy.http import Request
from cnki.items import CnkiListPassItem
from cnki.items import CnkiKeyWordItem
from cnki.spiders.mysql import Mysql

class CnkiListSpider(scrapy.Spider):
    mysql=Mysql()
    name = 'abstract'
    cookie={}
    keyword=''
    page=1
    allPage=1
    allowed_domains = ['']
    start_urls = ['']

    def parse(self, response):

        pass


