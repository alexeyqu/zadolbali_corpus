# -*- coding:utf8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class StoriesSpider(CrawlSpider):
    name = 'stories'
    allowed_domains = ['zadolba.li']
    start_urls = ['http://zadolba.li/']

    rules = (
        Rule(LinkExtractor(allow=('[0-9]{8}', ))),

        Rule(LinkExtractor(allow=('story/[0-9]+', )), callback='parse_story')
    )

    def parse_story(self, response):
        story_id = response.url.split("/")[-1]
        filename = 'stories.txt'# % page
        with open(filename, 'a') as f:
            f.write(story_id + '\n')
        self.log('Crawled story %s' % story_id)