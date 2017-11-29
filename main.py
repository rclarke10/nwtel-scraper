from scrapy.http import FormRequest
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import scrapy
import json
from src.DataUsageItem import DataUsage
from src.DataUsagePipeline import DataUsagePipeline
from src.DataUsageSpider import NwtelSpider
    
if __name__ == "__main__":
    #initialize crawler
    process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
      'LOG_ENABLED': 'True',
      'ITEM_PIPELINES': {
        'main.DataUsagePipeline': 300,
      }
    })

    #start crawler, blocks until it returns
    process.crawl(NwtelSpider)
    process.start()

    try:
      #read json file
      data = json.load(open('usage.json'))
      #print usage stats to screen
      print("Usage:        " + str(data['data_usage']) + " GB")
      print("Data Cap:     " + str(data['data_cap']) + " GB")
      print("Overage cost: $" + str(data['cost']))
      print("Percent Used: " + str(round(data['percent_used']*100,1)) + "%")
    except Exception as ex:
      print("Unexpected error: " + ex)