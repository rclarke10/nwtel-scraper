from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.spiders import Spider
from scrapy.utils.response import open_in_browser
from scrapy.selector import HtmlXPathSelector

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
                                    callback=self.getUsage)

  def getUsage(self, response):
    hxs = HtmlXPathSelector(response)
    #grabs usage
    usage = hxs.select('//a/text()').extract()[2]
    #grabs cap
    cap = hxs.select('//td/text()').extract()[0]
    #grabs amount over charged
    cost = hxs.select('//td/text()').extract()[1]

    usageNum = usage.split(' ')[0]

    capNum = cap.split(' ')[0]

    percentUsed = round(float(usageNum)*100/float(capNum),1)

    total = {'dataUsage':usageNum, 
             'dataCap':capNum, 
             'overageCost':cost, 
             'percentUsed': percentUsed}

  
    print("\n\n\n",total)






    #current usage XPATH: /html/body/table[1]/tbody/tr[3]/td[1]/a
    #current cap XPATH:   /html/body/table[1]/tbody/tr[3]/td[2]