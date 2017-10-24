# -*- coding:utf8 -*-

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector, Selector
from zadolbali.items import StoryItem

class StoryLoader(ItemLoader):
    default_output_processor = Join(' ')

class StoriesSpider(CrawlSpider):
    name = 'stories'
    allowed_domains = ['zadolba.li']
    start_urls = ['http://zadolba.li/']

    rules = (
        Rule(LinkExtractor(allow=('/[0-9]{8}', )), callback='parse_day', follow=True),
    )

    def parse_day(self, response):
        for url in response.xpath('//div[@class="story"]/h2/a/@href').extract():
            request = Request(StoriesSpider.start_urls[0] + str(url)[1:], callback=self.parse_story)
            request.meta['date'] = response.url.split('/')[-1]
            yield request

    def parse_story(self, response):
        hxs = HtmlXPathSelector(response)
        loader = StoryLoader(StoryItem(), hxs)

        loader.add_xpath('id', '//div[@class="story"]/div[@class="id"]/span/text()')
        loader.add_xpath('title', '//div[@class="story"]/h1/text()')
        loader.add_value('published', str(response.request.meta['date']))
        loader.add_xpath('tags', '//div[@class="story"]/div[@class="meta"]/div[@class="tags"]/ul/li/a/@href')
        loader.add_xpath('text', 'string(//div[@class="story"]/div[@class="text"])')
        loader.add_xpath('likes', 'string(//div[@class="story"]/div[@class="actions"]//div[@class="rating"])')
        loader.add_value('url', str(response.url))

        return loader.load_item()