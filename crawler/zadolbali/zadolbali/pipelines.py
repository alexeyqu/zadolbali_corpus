# -*- coding: utf-8 -*-

import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Session
from zadolbali.items import StoryItem
from scrapy.exceptions import DropItem

Base = declarative_base()

class StoryTable(Base):
	__tablename__ = 'Stories'
	id = Column(Integer, primary_key=True)
	story_id = Column(Integer)
	title = Column(String)
	# published = Column(String) datatype?
	# tags = Column(String)
	# text = Column(String)
	# likes = Column(Integer)

	def __init__(self, story_id, title):
		self.story_id = story_id
		self.title = title

	def __repr__(self):
		return "<Story %s, %s>" % \
			   (str(self.id), self.title)

class RedactorPipeline(object):
	def process_item(self, item, spider):
		for i, string in enumerate(item['title']):
			item['title'][i] = string.replace(u'\xa0', u' ').strip()
		for i, string in enumerate(item['text']):
			item['text'][i] = string.replace(u'\xa0', u' ').strip()
		return item

Base = declarative_base()

class SQLitePipeline(object):
	def __init__(self):
		basename = 'stories.sqlite'
		self.engine = create_engine("sqlite:///%s" % basename, echo=False)
		if not os.path.exists(basename):
			Base.metadata.create_all(self.engine)

	def process_item(self, item, spider):
		if isinstance(item, StoryItem):
			dt = StoryTable(item['id'],item['title'])
			self.session.add(dt)
		return item

	def close_spider(self, spider):
		self.session.commit()
		self.session.close()

	def open_spider(self, spider):
		self.session = Session(bind=self.engine)