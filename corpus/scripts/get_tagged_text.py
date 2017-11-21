import os, logging
import re
import nltk
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker

logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()

class Story(object):
    pass

class PosTagEntry(object):
    pass

def get_tagged_story(story_id, session):
    story = session.query(Story).get(story_id)
    pos_tags = session.query(PosTagEntry).filter(PosTagEntry.story_id == story_id).all()
    tagged_text = ''

    pos_tags.sort(key=lambda x: x.start)
    tag_id = 0

    for index, symbol in enumerate(story.text):
        if tag_id < len(pos_tags) and pos_tags[tag_id].end == index:
            tagged_text += '<' + pos_tags[tag_id].tag + '>'
            tag_id += 1
        tagged_text += symbol

    # print(story.text)
    # print(tagged_text)
    return tagged_text

if __name__ == "__main__":
    dbPath = '../stories.sqlite'
    engine = create_engine('sqlite:///%s' % dbPath, echo=True)
 
    metadata = MetaData(engine)
    DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    bookmarks = Table('stories', metadata, autoload=True)
    mapper(Story, bookmarks)

    bookmarks = Table('pos_tags', metadata, autoload=True)
    mapper(PosTagEntry, bookmarks)

    Session = sessionmaker(bind=engine)
    session = Session()
	
    print(get_tagged_story(2, session))