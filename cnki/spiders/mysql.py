import pymysql.cursors
from scrapy import cmdline
# 连接数据库
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='cnki',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor()

    # 关键字操作

    #获取关键字
    def getKeyWord(self):
        sql = "SELECT word from keyword  WHERE search=0 and num=(select max(num) from keyword where  search=0 ) "
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]


    #搜索结束之后的关键字设置搜索过
    def updateKeyWord(self,keyword):
        sql="update keyword set search=1 where word=%s"
        params=(keyword)
        self.cursor.execute(sql, params)
        self.connect.commit()
    #关键字插入数据库
    def insertKeyWord(self,key):
        if len(key):
            sql="INSERT INTO keyword  VALUES (NULL,%s,1,0,now())  ON DUPLICATE KEY UPDATE num=num+1"
            params=(key)
            self.cursor.execute(sql,params)
            self.connect.commit()
    # 论文链接操作

    #插入论文链接

    def insertPassList(self,item):
        sql="insert into url_list values(NUll,%s,%s,%s,%s,%s,%s,%s,1,0,%s,now()) ON DUPLICATE KEY UPDATE num=num+1"
        params=(item['url'],item['name'],item['pubdata'],item['cite'],item['citeUrl'],item['download'],item['source'],item['type'] )
        self.cursor.execute(sql,params)
        self.connect.commit()

    def startSpider(self,name):
        con = "scrapy crawl " + name
        print(con+" "+con)
        cmdline.execute(con.split())
