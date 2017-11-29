from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.spiders import Spider
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.crawler import Crawler
import json

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        results.append(dict(item))

class NwtelSpider(Spider):
  name = "nwtel"
  allowed_domains = ["nwtel.ca"]
  start_urls = ["https://ubbapps.nwtel.ca/cable_usage/secured/index.jsp"]

  def parse(self, response):
    formdata = {'j_target_url':'secured/index.jsp', #some default post url used
                'MAC':'c8fb26a159ee', #mac addresss
                'j_username':'C8FB26A159EE', #seems to just capitalize MAC address correctly
                'j_password':'123456'} #some default password used
    yield FormRequest.from_response(response,
                                    formdata=formdata,
                                    formnumber=0,
                                    callback=self.get_usage)

  def get_usage(self, response):
    selector = Selector(response)
    #grabs current data usage, data cap and current overage cost
    usage = selector.xpath('//a/text()').extract()[2]
    cap = selector.xpath('//td/text()').extract()[0]
    cost = selector.xpath('//td/text()').extract()[1]

    #convert formatted text to numbers to 3 decimal places
    usage_float = round(float(usage.split(' ')[0]),3)
    cap_float = round(float(cap.split(' ')[0]),3)

    #calc percent used
    percent_used = round(usage_float / cap_float , 3)

    #remove $ from cost
    cost = cost[1:]
    
    #construct dict containing usage stats
    stats = {'data_usage': usage_float, 
             'data_cap': cap_float, 
             'overage_cost': cost, 
             'percent_used': percent_used}
    
    #dump to usage.json
    with open('usage.json', 'w') as file:
      json.dump(stats, file)
    
if __name__ == "__main__":
    #initialize crawler
    process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
      'LOG_ENABLED': 'False'
    })

    #start crawler, blocks until it returns
    process.crawl(NwtelSpider)
    process.start()

    #try to print usage stats
    try:
      #read json file
      data = json.load(open('usage.json'))
      print("Usage:        " + str(data['data_usage']) + " GB")
      print("Data Cap:     " + str(data['data_cap']) + " GB")
      print("Overage cost: $" + str(data['overage_cost']))
      print("Percent Used: " + str(round(data['percent_used']*100,1)) + "%")
    except Exception as ex:
      print("Unexpected error: " + ex)