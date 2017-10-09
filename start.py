import time
from scrapy import cmdline
from cnki.spiders.cnki_one import CnkiOneSpider
from cnki.spiders.cnki_pass import CnkiPassSpider
from scrapy.crawler import CrawlerProcess
#注意，命令行保存的csv文件直接用excel打开可能会乱码，需要用其他工具（如notepad++）已UTF-8+BOM编码保存才能正常显示
#
cmdline.execute("scrapy crawl cnkiOne".split())
# from twisted.internet import reactor
# import scrapy
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging



# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# runner = CrawlerRunner()
#
# d = runner.crawl(CnkiOneSpider)
# d.addBoth(lambda _: reactor.stop())
# reactor.run() # the script will block here until the crawling is finished
# reactor.run()

# process = CrawlerProcess()
# process.crawl(CnkiOneSpider)
# process.start()
# for t in range(1,100):
#     process.stop()
#     process = CrawlerProcess()
#     process.crawl(CnkiPassSpider)
#     process.start()

