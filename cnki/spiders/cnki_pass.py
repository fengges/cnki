# -*- coding: utf-8 -*-
import scrapy


class CnkiPassSpider(scrapy.Spider):
    name = 'cnki_pass'
    allowed_domains = ['http://www.cnki.net']
    start_urls = ['http://www.cnki.net/']

    def parse(self, response):
        pass
