# -*- coding: utf-8 -*-
import scrapy
import codecs
import urllib
import time
import re
import json
import start
from scrapy.http import Request
from cnki.items import CnkiListPassItem
from cnki.items import CnkiKeyWordItem
from cnki.spiders.mysql import Mysql

class CnkiOneSpider(scrapy.Spider):
    name = 'cnkiOne'
    mysql = Mysql()
    cookie={}
    keyword=''
    page=1
    allPage=1
    allowed_domains = ['http://www.cnki.net','www.cnki.net','kns.cnki.net','http://www.baidu.com','www.baidu.com','search.cnki.net']
    start_urls = ['http://www.cnki.net']
    def getKeyWord(self):
        if len(self.keyword)==0:
            self.keyword=self.mysql.getKeyWord()
            print("new + word : ",self.keyword)
            return self.keyword
        else :
            return self.keyword

    def parse(self, response):
        keyword=urllib.parse.quote(self.getKeyWord())
        url = "http://kns.cnki.net/kns/request/SearchHandler.ashx?timestamp="+str(time.time())+"&action=&NaviCode=*&ua=1.11&PageName=ASP.brief_default_result_aspx&DbPrefix=SCDB&DbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&db_opt=CJFQ%2CCJRF%2CCDFD%2CCMFD%2CCPFD%2CIPFD%2CCCND&txt_1_sel=SU%24%25%3D%7C&txt_1_value1=" + keyword + "&txt_1_special1=%25&his=0&parentdb=SCDB&__=Tue%20Sep%2026%202017%2019%3A43%3A16%20GMT%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)"
        self.getCookie(response)
        yield scrapy.Request(url, cookies=self.cookie, callback=self.spider_keyWord)

    def spider_keyWord(self, response):
        keyword=urllib.parse.quote(self.getKeyWord())
        url="http://search.cnki.net/sug/su.ashx?action=getsmarttips&kw="+keyword+"&t=%E4%B8%BB%E9%A2%98&dbt=SCDB&attr=1&p=0.8080994242046629&td="+str(time.time())
        self.getCookie(response)
        yield scrapy.Request(url, cookies=self.cookie, callback=self.spide_list)

    def spide_list(self, response):
        item=CnkiKeyWordItem()
        word=str(response.body,'utf-8').replace("var oJson=",'',1).replace("'",'"',)
        python_obj = json.loads(word)
        item['word']=python_obj['sug']
        yield item
        keyword = urllib.parse.quote(self.getKeyWord())
        url="http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t="+str(time.time())+"&keyValue="+keyword+"S=1"
        self.getCookie(response)
        yield scrapy.Request(url, cookies=self.cookie, callback=self.spide_list_page)

    def spide_list_page(self, response):
        num = response.xpath("//div[@class='pagerTitleCell']/text()").extract()[0]
        # print(str(response.body,'utf-8'))
        num = int(re.sub(r'\D', "", num))
        self.allPage = num / 50
        if num % 50 != 0:
            self.allPage += 1
        if self.allPage > 120:
            self.allPage = 120
        print("all page",self.allPage)
        url=self.getPageUrl(response)
        self.getCookie(response)
        yield scrapy.Request(url, cookies=self.cookie,dont_filter=True, callback=self.prase_list)

    def prase_list(self,response):
       # print(str(response.body,"utf-8"))
        if "vericode.aspx" in response.url:
            print("sleep 1 miutues---------")
            self.goSleep(60)
            yield scrapy.Request("http://www.baidu.com?time="+str(time.time()), callback=self.parse)
        else:
            pass_list = response.xpath("//table[@class='GridTableContent']/tr[not(@class)]")
            for passage in pass_list:
                try:
                    item=CnkiListPassItem()
                    item['url'] = self.setValue(passage.xpath('./td[2]/a/@href'))
                    name =self.setValue(passage.xpath("./td[2]/a"))
                    item['name'] = self.getName(name)
                    item['source']=self.setValue(passage.xpath("./td[4]/a/text()"))
                    item['pubdata'] = self.setValue(passage.xpath("./td[5]/text()")).strip()
                    cite=passage.xpath("./td[7]/span/a")
                    if len(cite):
                        item['citeUrl']=self.setValue(cite.xpath("./@onclick"))
                        item['cite'] = self.setValue(cite.xpath("./text()"))
                    else :
                        item['citeUrl']=""
                        item['cite']=0
                    item['download'] = self.setValue(passage.xpath("./td[8]/span/a/text()"))
                    item['type']=1
                    print(item)
                    break
                except:
                    pass
            self.page += 1
            if self.page > 2:
                self.page = 1
                self.mysql.updateKeyWord(self.getKeyWord())
                self.keyword = ''
                print("update keyword")
                # self.goSleep(60)
                self.getCookie={}
                startSpider("cnki_pass")
                return
                #yield scrapy.Request(self.start_urls[0],dont_filter=True,cookies=self.cookie , callback=self.parse)
            else :
                url = self.getPageUrl(response)
                yield scrapy.Request(url, cookies=self.cookie, callback=self.prase_list)
    def setValue(self,node):
        if len(node):
            return node.extract()[0]
        else :
            return ''
    def getPageUrl(self,response):
        url=""
        if self.page==1:
            keyword = urllib.parse.quote(self.getKeyWord())
            url = "http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t=" + str(time.time())+"&keyValue=" + keyword + "&S=1&queryid=0&skuakuid=0&turnpage=1&recordsperpage=50"
        else :
            url = "http://kns.cnki.net/kns/brief/brief.aspx?curpage=" + str(self.page) + "&RecordsPerPage=50&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx&sKuaKuID=0&t="+ str(time.time())
        self.getCookie(response)
        print("page : "+str(self.page))
        return url

    def getName(self,name):
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', name)
        return dd

    def goSleep(self,t):
        for i in range(1,t):
             # print("sleep "+str(i)+" seconds")
            time.sleep(1)
    def getCookie(self,response):
        cookie2 = response.headers.getlist('Set-Cookie')
        for b in cookie2:
            str1= str(b,"utf-8")
            intdex=str1.index('=')
            self.cookie[str1[0:intdex]]=str1[intdex+1:]