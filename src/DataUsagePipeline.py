import scrapy
import json

class DataUsagePipeline(object):
  def open_spider(self, spider):
    #open file on spider start
    self.file_history = open('history.log', 'a')
    self.file_current_reading = open('last.json', 'w')

  def close_spider(self, spider):
    #close files when spider done
    self.file_history.close()
    self.file_current_reading.close()

  def process_item(self, item, spider):    
    #dump to usage.log
    entry = json.dumps(dict(item)) + "\n"
    self.file_history.write(entry)
    self.file_current_reading.write(entry)
    return item