# -*- coding: utf-8 -*-
import scrapy
import codecs
import urllib
import time
import re
import json

from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from cnki.spiders.mysql import Mysql

class CnkiOneSpider(scrapy.Spider):
    name = 'chenruitest'
    allowed_domains = ['http://www.cnki.net','www.cnki.net','kns.cnki.net','http://www.baidu.com','www.baidu.com','search.cnki.net']
    start_urls = ['http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201501&filename=1015000481.nh&v=MjY1MDNVUkwyZVorZHVGeTNuVnJyTVZGMjZHN080SHRYRXJwRWJQSVI4ZVgxTHV4WVM3RGgxVDNxVHJXTTFGckM=']
    dbcode = ''
    filename = ''
    dbname = ''


    def setVariable(self,url):
        self.dbcode = re.findall(r"dbcode=(.*)&dbname" , url)[0]
        self.filename = re.findall(r"filename=(.*)&v=" , url)[0]
        self.dbname = re.findall(r"dbname=(.*)&filename", url)[0]

    def parse(self, response):
        self.setVariable(self.start_urls[0])
        print (self.dbcode)
        print (self.filename)
        print (self.dbname)

        newURL = "http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode="+self.dbcode+"&filename="+self.filename+"&dbname="+self.dbname+"&RefType=1&vl=&CurDBCode=CJFQ&page=1"

        print (newURL)
        yield scrapy.Request(newURL, callback=self.getReferURL)


    def getReferURL(self,response):
        # print (str(response.body,'utf-8'))

        #中国学术期刊网络出版总库
        sum = response.xpath("//div[@class='author']/span/a/text()").extract()


