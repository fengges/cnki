import pymysql.cursors

# 连接数据库
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='cnki',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor()

    # 关键字操作

    #获取关键字
    def getKeyWord(self):
        sql = "SELECT word from keyword  WHERE search=0 and id=(select max(id) from keyword where  search=0 ) "
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]


    # 论文链接操作

    #插入论文链接

    def insertPassList(self,item):
        sql="insert into url_list values(NUll,%s,%s,1,now())"
        params=(item['url'],item['name'])
        #self.cursor.execute(sql,params)
        # self.connect.commit()