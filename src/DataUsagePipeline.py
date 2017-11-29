import scrapy
import json

class DataUsagePipeline(object):
  def open_spider(self, spider):
    #open file on spider start
    self.file = open('usage.json', 'w')

  def close_spider(self, spider):
    #close file when spider done
    self.file.close()

  def process_item(self, item, spider):    
    #dump to usage.json
    line = json.dumps(dict(item)) + "\n"
    self.file.write(line)
    return item