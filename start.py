from scrapy import cmdline

#注意，命令行保存的csv文件直接用excel打开可能会乱码，需要用其他工具（如notepad++）已UTF-8+BOM编码保存才能正常显示
cmdline.execute("scrapy crawl cnkiOne".split())

def startSpider(name):
    con="scrapy crawl "+name
    cmdline.execute(con.split())
