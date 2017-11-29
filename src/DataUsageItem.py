import scrapy

class DataUsage(scrapy.Item):
  data_usage = scrapy.Field()
  data_cap = scrapy.Field() 
  cost = scrapy.Field() 
  percent_used = scrapy.Field() 