# -*- coding: utf-8 -*-
import scrapy
import codecs
import urllib
import time
import re
import json

from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from cnki.items import *
from cnki.spiders.mysql import Mysql

class CnkiOneSpider(scrapy.Spider):
    name = 'cnkiOne'
    mysql = Mysql()
    id=""
    dbcode=''
    code=''
    key=''
    url=''
    allpage=0
    allowed_domains = ['http://www.cnki.net','www.cnki.net','kns.cnki.net','http://www.baidu.com','www.baidu.com','search.cnki.net']
    start_urls = ['http://www.cnki.net']

    def parse(self, response):
        item=self.mysql.getPassCiteUrl()
        print(item)
        self.id=item[0]
        self.url=item[1]
        self.dbcode=self.getKeyValue(item[2],'sdb')
        self.code = self.getKeyValue(item[2],'scode')
        self.key = self.getKeyValue(item[2],'skey')
        url=self.getUrl(1,'')
        yield scrapy.Request(url,callback=self.spider_cite)

    def spider_cite(self, response):
        #中国优秀硕士学位论文全文数据库
        citeList=response.xpath("//a[@target='kcmstarget']")
        for url in citeList:
            item = CnkiListPassItem()
            item['url'] = 'http://kns.cnki.net'+self.setValue(url.xpath('./@href'),'')
            item['name'] = self.setValue(url.xpath("./text()"),'')
            item['citeUrl'] = self.url
            item['download']='0'
            item['pubdata']=''
            item['source']=''
            item['cite']=0
            item['type'] = 2
            item['num'] = 5
            citeItem = CnkiCiteItem()
            citeItem['citeId'] = self.id
            citeItem['citeUrl'] = item['url']
            citeItem['type'] = 2
            yield citeItem
            yield item
        if 'page=' in response.url:
            pass
        else:
            numList = response.xpath("//span[@name='pcount']")
            for num in numList:
                self.allpage =self.getAllpage(int(self.setValue(num.xpath('./text()'),0)),10)
                curdbcode=num.xpath('./@id').extract()[0][3:]
                for  p in range(2,int(self.allpage+1)):
                    url = self.getUrl(p, curdbcode)
                    yield scrapy.Request(url, callback=self.spider_cite)
            self.mysql.updatePassList(self.id,1)
            yield scrapy.Request(self.start_urls[0],dont_filter=True, callback=self.parse)

    def getAllpage(self,num,pagesize):
        size = num/pagesize
        if num % pagesize != 0:
            size += 1
        return size

    def setValue(self,node,value):
        if len(node):
            return node.extract()[0]
        else :
            return value
    def getUrl(self,page,curdbcode):
        url=''
        if page!=1:
            url="http://kns.cnki.net/kcms/detail/frame/asynlist.aspx?dbcode="+self.dbcode+"&CurDBCode="+curdbcode+"&search="+self.key+"&code="+self.code+"&ds=frame/list.aspx&reftype=18&page="+str(page)
        else:
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