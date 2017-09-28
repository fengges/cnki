# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from cnki.items import CnkiListPassItem
from cnki.spiders.mysql import Mysql

class CnkiPipeline(object):
    mysql=Mysql()
    def process_item(self, item, spider):
        if type(item)==CnkiListPassItem:
            self.cnkiList(item)
            return item

    def cnkiList(self,item):
        item['url']=item['url'].replace("/kns","http://kns.cnki.net/KCMS",1)
        self.mysql.insertPassList(item)

    def cnkiPass(self,item):
        pass
