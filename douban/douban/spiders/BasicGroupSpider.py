# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 13:08:58 2015

"""
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.item import Item
from douban.items import DoubanItem
from scrapy.selector import HtmlXPathSelector
import re

class GroupTestSpider(Spider):
    name = "Test"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://www.douban.com/group/WHV",
    ]
 
    def parse(self, response):
        self.log("Fetch douban homepage page: %s" % response.url)
        #open("test.html", "wb").write(response.body)
        hxs=HtmlXPathSelector(response)
        item=DoubanItem()
        
        #get group name
        item['GroupName']=hxs.xpath('//h1/text()').re("^\s+(.*)\s+$")  #.extract() # re 去掉空格？
        
        #get group url
        item['GroupURL']=response.url

        #get relative groups
        item['RelativeGroups']=[]
        groups=hxs.xpath('//div[contains(@class,"group-list-item")]')
        for group in groups:
            url=group.select('.//div[contains(@class,"title")]/a/@href').extract()
            item['RelativeGroups'].append(url)
        return item
       
'''note...
try中是import Spider，若在class中写GroupTestSpider(BaseSpider)会有警告，改BaseSpider as Spider
GroupTestSpider(Spider)中统一用Spider


.//div[] or div[] ,not //div[],结果会重复12次
...note'''