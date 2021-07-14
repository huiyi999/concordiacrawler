from scrapy import cmdline

name = 'concordia'
# cmd = 'scrapy crawl {0} -s CLOSESPIDER_PAGECOUNT=100'.format(name)
cmd = 'scrapy crawl {0} -s CLOSESPIDER_ITEMCOUNT=100'.format(name)
cmdline.execute(cmd.split())
