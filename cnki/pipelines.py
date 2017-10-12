# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from cnki.items import *
from cnki.spiders.mysql import Mysql

class CnkiPipeline(object):
    #FFFFFFF
    mysql=Mysql()
    def process_item(self, item, spider):
        if type(item)==CnkiListPassItem:
            self.cnkiList(item)

        elif type(item)==CnkiKeyWordItem:
            self.cnkiKeyWord(item)

        elif type(item) == CnkiAbstractItem:
            self.cnkiCnkiAbstract(item)
        elif type(item) == CnkiCiteItem:
            self.cnkiCnkiCite(item)
        elif type(item) == CnkiKeyItem:
            self.cnkiKey(item)

        return item
    def cnkiKey(self,item):
        self.mysql.insertKey(item)
    def cnkiList(self,item):
        item['url']=item['url'].replace("/kns","http://kns.cnki.net/KCMS",1)
        if len(item['download']):
            pass
        else :
            item['download']=0
        item['citeUrl'] = item['citeUrl'].replace("TPI_openwindow('","http://kns.cnki.net").replace( "'aaa','status=yes,scrollbars=yes',event)",'').strip().replace("',","")
        self.mysql.insertPassList(item)

    def cnkiKeyWord(self,item):
        key=item['word'].split(';')
        for k in key:
            k = k.strip()
            self.mysql.insertKeyWord(k,item['num'])

    def cnkiCnkiAbstract(self,item):
        self.mysql.insertPassAbstract(item)
        self.mysql.updatePassList(item['id'],100)
        pass

    def cnkiCnkiCite(self,item):
        self.mysql.insertCite(item)

