# -*- coding: utf-8 -*-

import os, logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from scrapy.exceptions import DropItem
from scrapy import signals
from zadolbali.items import StoryItem

logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()

class Story(DeclarativeBase):
	__tablename__ = 'stories'

	id = Column('id', Integer, primary_key=True)
	title = Column('title', String)
	published = Column('published', Integer)
	tags = Column('tags', String)
	text = Column('text', String)
	likes = Column('likes', Integer)

	def __repr__(self):
		return "<Story({0}, {1})>".format(self.id, self.title)

class RedactorPipeline(object):
	def process_item(self, item, spider):
		item['id'] = int(item['id']) 
		item['title'] = item['title'].replace(u'\xa0', u' ').strip()
		item['published'] = int(item['published']) 
		item['tags'] = ' '.join(tag.split('/')[2] for tag in item['tags'].split())
		item['text'] = item['text'].replace(u'\xa0', u' ').strip()
		item['likes'] = int(item['likes'])
		return item

class SqlitePipeline(object):
	def __init__(self, settings):
		self.database = settings.get('DATABASE')
		self.sessions = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls(crawler.settings)
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def create_engine(self):
		engine = create_engine(URL(**self.database), poolclass=NullPool)
		return engine

	def create_tables(self, engine):
		DeclarativeBase.metadata.create_all(engine, checkfirst=True)

	def create_session(self, engine):
		session = sessionmaker(bind=engine)()
		return session

	def spider_opened(self, spider):
		engine = self.create_engine()
		self.create_tables(engine)
		session = self.create_session(engine)
		self.sessions[spider] = session

	def spider_closed(self, spider):
		session = self.sessions.pop(spider)
		session.close()

	def process_item(self, item, spider):
		session = self.sessions[spider]
		story = Story(**item)
		link_exists = session.query(Story).filter_by(id=item['id']).first() is not None

		if link_exists:
			logger.info('Item {} is in db'.format(story))
			return item

		try:
			session.add(story)
			session.commit()
			logger.info('Item {} stored in db'.format(story))
		except:
			logger.info('Failed to add {} to db'.format(story))
			session.rollback()
			raise

		return item