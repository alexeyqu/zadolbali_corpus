# -*- coding: utf-8 -*-

from scrapy import Item, Field

class StoryItem(Item):
    id = Field()
    title = Field()
    published = Field()
    tags = Field()
    text = Field()
    likes = Field()
    pass
