# -*- coding: utf-8 -*-
import scrapy
import json
from .. import settings
from .. import items
START_URL = 'http://image.so.com/zj?ch={}&sn={}&listtype=new&temp=1'
class ImageSpider(scrapy.Spider):
    name = 'image'
    total = 0

    # allowed_domains = ['image.so.com']
    # start_urls = ['http://image.so.com/']
    def start_requests(self):
        yield scrapy.Request(START_URL.format(settings.KEYWORD,0),callback=self.parse)
    def parse(self, response):
        res = json.loads(response.text)
        item = items.ImgItem()
        for img in res['list']:
            item['image_urls'] = [img.get('qhimg_url')]
            yield item
        self.total += res['count']
        if self.total<settings.MAX_NUM and res['count'] > 0:
            url = START_URL.format(settings.KEYWORD, self.total)
            yield scrapy.Request(url=url,callback=self.parse)