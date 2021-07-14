# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json
import os



class ConcordiacrawlerPipeline:
    def __init__(self):
        self.file = codecs.open('concordia.json', 'w+', 'utf-8')

    def open_spider(self, spider):

        self.file.write('[\n')

    def process_item(self, item, spider):

        lines = json.dumps(dict(item), ensure_ascii=False)
        self.file.write('\t' + lines + ',\n')
        return item

    def close_spider(self, spider):
        self.file.seek(-2, os.SEEK_END)
        self.file.truncate()
        self.file.write('\n]')
        self.file.close()

