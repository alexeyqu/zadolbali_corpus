# -*- coding:utf8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.loader.processor import Identity
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector, Selector
from zadolbali.items import StoryItem

class StoryLoader(XPathItemLoader):
    default_output_processor = Identity()

class StoriesSpider(CrawlSpider):
    name = 'stories'
    allowed_domains = ['zadolba.li']
    start_urls = ['http://zadolba.li/']

    rules = (
        Rule(LinkExtractor(allow=('[0-9]{8}', ))),

        Rule(LinkExtractor(allow=('story/[0-9]+', )), callback='parse_story')
    )

    def parse_story(self, response):
        hxs = HtmlXPathSelector(response)
        loader = StoryLoader(StoryItem(), hxs)

        loader.add_xpath('id', '//div[@class="story"]/div[@class="id"]/span/text()')
        loader.add_xpath('title', '//div[@class="story"]/h1/text()')
        loader.add_xpath('published', '//div[@class="story"]/div[@class="meta"]/div[@class="date-time"]/text()')
        loader.add_xpath('tags', '//div[@class="story"]/div[@class="meta"]/div[@class="tags"]/ul/li/a/@href')
        loader.add_xpath('text', 'string(//div[@class="story"]/div[@class="text"])')
        loader.add_xpath('likes', '//div[@class="story"]/div[@class="actions"]/div[@class="button-group like"]/a[@class="button"]/div[@class="rating"]/span/text()')

        return loader.load_item()