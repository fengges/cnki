import pymysql.cursors
# 连接数据库
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Cr648546845',
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
    def insertKeyWord(self,key,num):
        if len(key):
            sql="INSERT INTO keyword  VALUES (NULL,%s,"+str(num)+",0,now())  ON DUPLICATE KEY UPDATE num=num+1"
            params=(key)
            self.cursor.execute(sql,params)
            self.connect.commit()


    # 论文链接操作

    #插入论文链接
    def insertPassList(self,item):
        sql="insert into url_list values(NUll,%s,%s,%s,%s,%s,%s,%s,%s,0,%s,now()) ON DUPLICATE KEY UPDATE num=num+1"
        params=(item['url'],item['name'],item['pubdata'],item['cite'],item['citeUrl'],item['download'],item['source'],item['num'],item['type'] )
        self.cursor.execute(sql,params)
        self.connect.commit()

    #搜索后更新状态
    def updatePassList(self, id,add):
        sql = "update url_list set search=search+"+str(add)+" where id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        self.connect.commit()

    #获取论文引用
    def getPassCiteUrl(self):
        sql = "SELECT id,url,cite_url from url_list  WHERE length(cite_url)!=0 and (mod(search,2)=0) and type=1 and num=(select max(num) from url_list where length(cite_url)!=0 and type=1 and (mod(search,2)=0) )"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    # 获取论文摘要链接
    def getPassAbstractUrl(self):
        sql = "SELECT id,url from url_list  WHERE (search =0 or search=1 ) and num=(select max(num) from url_list where search =0 or search=1 )"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def insertPassAbstract(self,item):
        sql="insert into abstract values(%s,%s,%s,%s,%s,now())"
        params=(item['id'],item['author'],item['organization'].strip(),item['abstract'],item['fund'] )
        self.cursor.execute(sql,params)
        self.connect.commit()


    def insertCite(self,item):
        sql="insert into cite values(null,%s,%s,%s,now())"
        params=(item['citeId'],item['citeUrl'],item['type'] )
        self.cursor.execute(sql,params)
        self.connect.commit()
