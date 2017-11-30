from scrapy.http import FormRequest
from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy
import json
from .DataUsageItem import DataUsage
from .Config import Config

class NwtelSpider(Spider):
  name = "nwtel"
  allowed_domains = ["nwtel.ca"]
  start_urls = ["https://ubbapps.nwtel.ca/cable_usage/secured/index.jsp"]
  

  def parse(self, response):
    mac_address = Config.get_mac()
    formdata = {'j_target_url':'secured/index.jsp', #some default post url used
                'MAC': mac_address, #mac addresss
                'j_username':mac_address, #seems to just capitalize MAC address correctly
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

    #send stats to DataUsage Item
    doc = DataUsage()
    doc['data_usage'] = usage_float
    doc['data_cap'] = cap_float
    doc['cost'] = cost
    doc['percent_used'] = percent_used
    yield doc