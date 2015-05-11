# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 22:41:22 2015

@author: Administrator
"""
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector #replace HtmlXPathSelector
from scrapy.http.request import Request
from douban.items import DoubanItem
import re

class GroupSpider(CrawlSpider):
    name='GroupSpider'
    allowed_domain=['douban.com']
    start_urls=[
    "http://www.douban.com/group/explore?tag=%E5%85%B4%E8%B6%A3", # catalog of groups, 兴趣
    "http://www.douban.com/group/explore?tag=%E7%94%9F%E6%B4%BB", # catalog of groups, 生活
    "http://www.douban.com/group/explore?tag=%E8%B4%AD%E7%89%A9",
    "http://www.douban.com/group/explore?tag=%E7%A4%BE%E4%BC%9A",
    "http://www.douban.com/group/explore?tag=%E8%89%BA%E6%9C%AF",
    "http://www.douban.com/group/explore?tag=%E5%AD%A6%E6%9C%AF",
    "http://www.douban.com/group/explore?tag=%E6%83%85%E6%84%9F",
    "http://www.douban.com/group/explore?tag=%E9%97%B2%E8%81%8A"  # catalog of groups, 闲聊
    ]
    
    rules=[Rule(SgmlLinkExtractor(allow=('/group/[^/]+/$', )), callback='parse_group_page'),
    ] #get the groups of the corresponding catalog
    
        
    def parse_group_page(self,response):
        self.log("Fetch douban page: %s" % response.url)
        hxs=Selector(response)
        item=DoubanItem()
        
        #get group name
        item['GroupName']=hxs.xpath('//h1/text()').re("^\s+(.*)\s+$")
        
        #get group url
        item['GroupURL']=response.url

        #get relative groups
        item['RelativeGroupNames']=[]
        item['RelativeGroupURLs']=[]
        groups=hxs.xpath('//div[contains(@class,"group-list-item")]')
        for group in groups:
            name=group.xpath('div[contains(@class,"title")]/a/@title').extract()
            url=group.xpath('.//div[contains(@class,"title")]/a/@href').extract()
            item['RelativeGroupNames'].append(name)
            item['RelativeGroupURLs'].append(url)
        return item
        