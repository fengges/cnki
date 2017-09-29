# -*- coding: utf-8 -*-
import scrapy
import codecs
import urllib
import time
import re

from scrapy.http import Request
from cnki.items import CnkiListPassItem
from cnki.spiders.mysql import Mysql

class CnkiPassSpider(scrapy.Spider):
    name = 'cnki_pass'
    mysql = Mysql()
    cookie = {}
    keyword = ''
    page = 1
    allPage = 1
    allowed_domains = ['http://www.cnki.net', 'kns.cnki.net', 'http://www.baidu.com', 'www.baidu.com']
    start_urls = ['http://www.cnki.net']

    def getKeyWord(self):
        if len(self.keyword) == 0:
            return self.mysql.getKeyWord()
        else:
            return self.keyword

    def parse(self, response):
        keyword = urllib.parse.quote(self.getKeyWord())
        url = "http://kns.cnki.net/kns/request/SearchHandler.ashx?timestamp=" + str(
            time.time()) + "&action=&NaviCode=*&ua=1.11&PageName=ASP.brief_default_result_aspx&DbPrefix=SCDB&DbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&db_opt=CJFQ%2CCJRF%2CCDFD%2CCMFD%2CCPFD%2CIPFD%2CCCND&txt_1_sel=SU%24%25%3D%7C&txt_1_value1=" + keyword + "&txt_1_special1=%25&his=0&parentdb=SCDB&__=Tue%20Sep%2026%202017%2019%3A43%3A16%20GMT%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)"
        self.getCookie(response)
        yield scrapy.Request(url, cookies=self.cookie, callback=self.spide_list)

    def spide_list(self, response):
        keyword = urllib.parse.quote(self.getKeyWord())
        url = "http://kns.cnki.net/kns/brief/brief.aspx?timestamp=" + str(
            time.time()) + "&pagename=ASP.brief_default_result_aspx&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t=1506415981955&keyValue=" + keyword + "S=1"
        self.getCookie(response)
        yield scrapy.Request(url, cookies=self.cookie, callback=self.spide_list_page)

    def spide_list_page(self, response):
        num=response.xpath("//div[@class='pagerTitleCell']/text()").extract()[0]
        num=int(re.sub(r'\D', "", num))
        self.allPage=num/50
        if num%50!=0:
            self.allPage+=1
        if self.allPage>120:
            self.allPage=120
        print(self.allPage)
        for num in range(1, 20):
            url = self.getPageUrl(response)
            self.page += 1
            yield scrapy.Request(url, cookies=self.cookie, dont_filter=True, callback=self.prase_list)

    def prase_list(self, response):
        # print(str(response.body,"utf-8"))
        if "vericode.aspx" in response.url:
            print("sleep ten miutues---------")
            time.sleep(1 * 60)
            yield scrapy.Request("http://www.baidu.com?time=" + str(time.time()), callback=self.parse)
        else:
            pass_list = response.xpath("//a[@class='fz14']")
            for passage in pass_list:
                try:
                    item = CnkiListPassItem()
                    item['url'] = passage.xpath('./@href').extract()[0]
                    name = passage.extract()
                    item['name'] = self.getName(name)
                    yield item
                except:
                    pass

    def getPageUrl(self, response):
        url = ""
        if self.page == 1:
            keyword = urllib.parse.quote(self.getKeyWord())
            url = "http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t=1506588228660&keyValue=" + keyword + "&S=1&queryid=0&skuakuid=0&turnpage=1&recordsperpage=50"
        else:
            url = "http://kns.cnki.net/kns/brief/brief.aspx?curpage=" + str(
                self.page) + "&RecordsPerPage=50&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx&sKuaKuID=0"
        self.getCookie(response)
        print(self.page)
        print(" page  " + url)
        return url

    def getName(self, name):
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', name)
        return dd

    def getCookie(self, response):
        cookie2 = response.headers.getlist('Set-Cookie')
        for b in cookie2:
            str1 = str(b, "utf-8")
            intdex = str1.index('=')
            self.cookie[str1[0:intdex]] = str1[intdex + 1:]