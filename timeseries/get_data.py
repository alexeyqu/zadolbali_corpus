from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

class Story(object):
    pass
 
def loadSession():
    dbPath = '../corpus/stories.sqlite'
    engine = create_engine('sqlite:///%s' % dbPath, echo=True)
 
    bookmarks = Table('stories', MetaData(engine), autoload=True)
    mapper(Story, bookmarks)
 
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 
if __name__ == "__main__":
    session = loadSession()
    res = session.query(Story).all()
    with open('data.csv', 'w') as data:
        for story in res:
            data.write('{0}\t{1}\t{2}\t{3}\n'.format(story.id, story.published, story.tags, story.likes))