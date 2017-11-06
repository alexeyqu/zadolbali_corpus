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

class PosTagEntry(DeclarativeBase):
    __tablename__ = 'pos_tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String)
    story_id = Column(Integer)
    start = Column(Integer)
    end = Column(Integer)

    def __repr__(self):
        return "<PosTagEntry({0}, {1}, {2}, {3}-{4})>".format(self.id, self.tag, self.story_id, self.start, self.end)

def tokenize_with_coords(text):
    return [(match.group(0), match.start(), match.end()) for match in re.finditer(r'[\w]+', text)]
 
if __name__ == "__main__":
    dbPath = '../stories.sqlite'
    engine = create_engine('sqlite:///%s' % dbPath, echo=True)
 
    metadata = MetaData(engine)
    DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    bookmarks = Table('stories', metadata, autoload=True)
    mapper(Story, bookmarks)

    Session = sessionmaker(bind=engine)
    session = Session()

    res = session.query(Story).all()

    for story in res:
        tokens = tokenize_with_coords(story.text)
        tagged_tokens = zip(tokens, nltk.pos_tag([token for token, start, end in tokens], lang='rus'))
        for tagged in tagged_tokens:
            print(tagged)
            tag_entry = PosTagEntry(tag=tagged[1][1], story_id=story.id, start=tagged[0][1], end=tagged[0][2])
            print(tag_entry)
            session.add(tag_entry)
        try:
            session.commit()
            logger.info('Item {} stored in db'.format(tag_entry))
        except:
            logger.info('Failed to add {} to db'.format(tag_entry))
            session.rollback()
            raise