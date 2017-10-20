# -*- coding: utf-8 -*-

class RedactorPipeline(object):
	def process_item(self, item, spider):
		for i, string in enumerate(item['title']):
			item['title'][i] = string.replace(u'\xa0', u' ').strip()
		for i, string in enumerate(item['text']):
			item['text'][i] = string.replace(u'\xa0', u' ').strip()
		return item