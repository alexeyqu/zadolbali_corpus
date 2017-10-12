# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StoryItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    published = scrapy.Field()
    tags = scrapy.Field()
    text = scrapy.Field()
    likes = scrapy.Field()
    pass
