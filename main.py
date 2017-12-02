from scrapy.crawler import CrawlerProcess
import scrapy
import json
from src.DataUsagePipeline import DataUsagePipeline
from src.DataUsageSpider import NwtelSpider
from src.Config import Config
import time
    
def ask_for_mac():
  #take MAC address input here

  #ask if to save and not ask in future? can manually change config later
  return 1

if __name__ == "__main__":
  #start timer (TODO add verbose flag in config)
  start = time.time()

  mac = ask_for_mac()

  #read config
  logging = Config.logging()

  #initialize crawler
  process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_ENABLED': logging,
    'ITEM_PIPELINES': {
      'main.DataUsagePipeline': 300,
    }
  })

  

  
  #start crawler, blocks until it returns
  process.crawl(NwtelSpider)
  process.start()

  try:
    time.sleep(1)
    #read json file
    data = json.load(open('last.json'))
    #print(data)
    #print usage stats to screen
    print("Usage:        " + str(data['data_usage']) + " GB")
    print("Data Cap:     " + str(data['data_cap']) + " GB")
    print("Overage cost: $" + str(data['cost']))
    print("Percent Used: " + str(round(data['percent_used']*100,1)) + "%")
  except Exception as ex:
    print({"error": ex})
  end = time.time()
  print("Execution took: " + str(round(end-start,1)) + "s")
  
  