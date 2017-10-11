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
    def getPassAbstractUrl(self):
        if len(self.PassAbstractUrl)==0:
            self.PassAbstractUrl=self.mysql.getPassAbstractUrl()
            print("new + word : ",self.PassAbstractUrl)
            return self.PassAbstractUrl
        else :
            return self.PassAbstractUrl

    def parse(self, response):
        url = self.getPassAbstractUrl()[1]
        self.PassId = self.getPassAbstractUrl()[0]
        print (url)
        yield scrapy.Request(url, callback=self.getAbstract)

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

            self.PassAbstractUrl = ''
            url = self.getPassAbstractUrl()[1]
            self.PassId = self.getPassAbstractUrl()[0]
            yield scrapy.Request(url, callback=self.getAbstract)
        except:
            self.mysql.updatePassList(self.PassId, 5)
            self.PassAbstractUrl = ''
            url = self.getPassAbstractUrl()[1]
            self.PassId = self.getPassAbstractUrl()[0]
            yield scrapy.Request(url, callback=self.getAbstract)

    def goSleep(self,t):
        for i in range(1,t):
             # print("sleep "+str(i)+" seconds")
            time.sleep(1)



