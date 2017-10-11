# -*- coding: utf-8 -*-
import scrapy
import codecs
import urllib
import time
import re
import json

from scrapy.http import Request
from cnki.items import *

from cnki.spiders.mysql import Mysql

class CnkiListSpider(scrapy.Spider):
    mysql=Mysql()
    name = 'cnki_abstract'
    start_urls = ['http://www.cnki.net']
    allowed_domains = ['http://www.cnki.net', 'www.cnki.net', 'kns.cnki.net','search.cnki.net']
    PassAbstractUrl = ''
    PassId = 0

    dbcode = ''
    filename = ''
    dbname = ''

    url = ''


    def getPassAbstractUrl(self):
        if len(self.PassAbstractUrl)==0:
            self.PassAbstractUrl=self.mysql.getPassAbstractUrl()
            print("new + word : ",self.PassAbstractUrl)
            return self.PassAbstractUrl
        else :
            return self.PassAbstractUrl

    def parse(self, response):
        self.PassAbstractUrl = ''
        url = self.getPassAbstractUrl()[1]
        self.PassId = self.getPassAbstractUrl()[0]
        # print (url)
        yield scrapy.Request(url, callback=self.getAbstract)
        try:
            self.setVariable(url)
            tui="http://kns.cnki.net/kcms/detail/frame/asynlist.aspx?dbcode="+self.dbcode+"&dbname="+self.dbname+"&filename="+self.filename+"&curdbcode=hehe&reftype=605&catalogId=lcatalog_func605&catalogName=%E8%AF%BB%E8%80%85%E6%8E%A8%E8%8D%90"
            yield scrapy.Request(tui, dont_filter=True, callback=self.parse_tui)

            newURL = self.getUrl(1, '')
            yield scrapy.Request(newURL, callback=self.getReferURL)
        except:
            self.mysql.updatePassList(self.PassId, 7)
            yield scrapy.Request(self.start_urls[0], dont_filter=True, callback=self.parse)



    def parse_tui(self,response):
        citeList = response.xpath("//a[@target='kcmstarget']")
        for url in citeList:
            item = CnkiListPassItem()
            item['url'] = 'http://kns.cnki.net' + self.setValue(url.xpath('./@href'), '')
            item['name'] = self.setValue(url.xpath("./text()"), '')
            item['citeUrl'] = self.url
            item['download'] = '0'
            item['pubdata'] = ''
            item['source'] = ''
            item['cite'] = 0
            item['type'] = 5
            citeItem = CnkiCiteItem()
            citeItem['citeId'] = self.PassId
            citeItem['citeUrl'] = item['url']
            citeItem['type'] = 5
            yield citeItem
            yield item
    def getAbstract(self,response):
        # print (str(response.body, 'utf-8'))
        item_abstract = CnkiAbstractItem()
        item_keyword = CnkiKeyWordItem()

        try:
            #ID
            item_abstract['id'] = self.PassId
            #作者
            item_abstract['author'] = ",".join(response.xpath("//div[@class='author']/span/a/text()").extract())
            # print ("name:",author)
            #机构
            # item_abstract['organization'] = ",".join(response.xpath("//div[@class='orgn']/span/a/text()").extract())
            organization = ",".join(response.xpath("//div[@class='orgn']/span/a/text()").extract())
            if len(organization)<255:
                item_abstract['organization'] = organization
            else:
                item_abstract['organization'] = ""
            # print ("organization:", organization)
            #摘要
            item_abstract['abstract'] = response.xpath("//span[@id='ChDivSummary']/text()").extract()[0]
            # print ("abstract:", abstract)
            #基金
            item_abstract['fund'] = ",".join(response.xpath("//label[@id='catalog_FUND']/following-sibling::*/text()").extract())
            # print ("fund：",fund)
            #关键词
            item_keyword['word'] = "".join(response.xpath("//label[@id='catalog_KEYWORD']/following-sibling::*/text()").extract())
            keyword = "".join(response.xpath("//label[@id='catalog_KEYWORD']/following-sibling::*/text()").extract())
            item_keyword['word'] = keyword.strip()
            item_keyword['num']=5


            yield item_keyword
            yield item_abstract

            # self.PassAbstractUrl = ''
            # url = self.getPassAbstractUrl()[1]
            # self.PassId = self.getPassAbstractUrl()[0]
            # yield scrapy.Request(url, callback=self.getAbstract)
        except:
            self.mysql.updatePassList(self.PassId, 7)
            # self.PassAbstractUrl = ''
            # url = self.getPassAbstractUrl()[1]
            # self.PassId = self.getPassAbstractUrl()[0]
            # yield scrapy.Request(url, callback=self.getAbstract)

    def getReferURL(self,response):
        # print (str(response.body,'utf-8'))

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
            item['type'] = 4
            citeItem = CnkiCiteItem()
            citeItem['citeId'] = self.PassId
            citeItem['citeUrl'] = item['url']
            citeItem['type'] = 4
            # print(item)
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
                    print(url)
                    yield scrapy.Request(url, callback=self.getReferURL)
            self.mysql.updatePassList(self.PassId,5)
            yield scrapy.Request(self.start_urls[0],dont_filter=True, callback=self.parse)


    def getAllpage(self, num, pagesize):
        size = num / pagesize
        if num % pagesize != 0:
            size += 1
        return size

    def setValue(self, node, value):
        if len(node):
            return node.extract()[0]
        else:
            return value
    def getUrl(self,page,curdbcode):
        url=''
        if page==1:
            url="http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode="+self.dbcode+"&filename="+self.filename+"&dbname="+self.dbname+"&RefType=1&vl="
        else:
            url="http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode="+self.dbcode+"&filename="+self.filename+"&dbname="+self.dbname+"&RefType=1&vl=&CurDBCode="+curdbcode+"&page="+str(page)
        return url

    def setVariable(self,url):

        self.dbcode = self.getKeyValue(url,'dbcode')
        self.filename =  self.getKeyValue(url,'filename')
        self.dbname =  self.getKeyValue(url,'dbname')

    def getKeyValue(self, url, key):
        try:
            index = url.index('?')
            query = url[index + 1:]
            paramList = query.split('&')
            for p in paramList:
                temp = p.split('=')
                if temp[0].lower() == key:
                    return temp[1]
        except:
            print(url)






