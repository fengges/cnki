# -*- coding: utf-8 -*-
import scrapy
import codecs
import urllib
import time
import re
import json

from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from cnki.items import CnkiListPassItem
from cnki.items import CnkiKeyWordItem
from cnki.spiders.mysql import Mysql

class CnkiOneSpider(scrapy.Spider):
    name = 'cnkiOne'
    mysql = Mysql()
    id=""
    dbcode=''
    code=''
    key=''
    allpageOne=0
    allowed_domains = ['http://www.cnki.net','www.cnki.net','kns.cnki.net','http://www.baidu.com','www.baidu.com','search.cnki.net']
    start_urls = ['http://www.cnki.net']

    def parse(self, response):
        item=self.mysql.getPassCiteUrl()
        self.id=item[0]
        self.dbcode=self.getKeyValue(item[1],'sdb')
        self.code = self.getKeyValue(item[1],'scode')
        self.key = self.getKeyValue(item[1],'skey')
        url=self.getUrl()
        yield scrapy.Request(url,callback=self.spider_cite)

    def spider_cite(self, response):
        #中国优秀硕士学位论文全文数据库
        num=self.setValue(response.xpath("//span[@id='pc_CMFD']"),0)
        citeList=response.xpath()

    def setValue(self,node,value):
        if len(node):
            return node.extract()[0]
        else :
            return value
    def getUrl(self):
        url="http://kns.cnki.net/kcms/detail/frame/asynlist.aspx?dbcode="+self.dbcode+"&curdbcode=&search="+self.key+"&code="+self.code+"&ds=frame/list.aspx&reftype=18"
        return url

    def getKeyValue(self,url,key):
        index=url.index('?')
        query=url[index+1:]
        paramList=query.split('&')
        for p in paramList:
            temp=p.split('=')
            if temp[0]==key:
                return temp[1]