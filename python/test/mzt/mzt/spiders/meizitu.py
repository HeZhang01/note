# -*- coding: utf-8 -*-
import scrapy
import os

# 图片属性
class PItem(scrapy.Item):
    image_urls = scrapy.Field()
    images     = scrapy.Field()
    name       = scrapy.Field()

# Spider start_urls:初始页面，parse:列表页,parse_item:项目页面
class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    start_urls = (
        'http://www.meizitu.com/a/list_1_1.html',
    )

    def parse(self, response):
        exp   = u'//div[@id="wp_page_numbers"]//a[text()="下一页"]/@href'
        _next = response.xpath(exp).extract_first()
        next_page = os.path.join(os.path.dirname(response.url), _next)
        yield scrapy.FormRequest(next_page, callback=self.parse)
        for p in response.xpath('//li[@class="wp-item"]//a/@href').extract():
            yield scrapy.FormRequest(p, callback=self.parse_item)


    def parse_item(self, response):
        item  = PItem()
        urls  = response.xpath("//div[@id='picture']//img/@src").extract()
        name  = response.xpath("//div[@id='picture']//img/@alt").extract()[0]
        item['image_urls'] = urls
        item['name']       = name.split(u', ')[0]
        return item


