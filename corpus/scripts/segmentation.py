from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
import nltk
 
class Story(object):
    pass
 
def loadSession():
    dbPath = '../stories.sqlite'
    engine = create_engine('sqlite:///%s' % dbPath, echo=True)
 
    bookmarks = Table('stories', MetaData(engine), autoload=True)
    mapper(Story, bookmarks)
 
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 
if __name__ == "__main__":
    session = loadSession()
    res = session.query(Story).all()
    all_text = ''
    for story in res:
        all_text += story.text
        all_text += ' '

    trainer = PunktTrainer()
    trainer.INCLUDE_ALL_COLLOCS = True
    trainer.train(all_text)
     
    tokenizer = PunktSentenceTokenizer(trainer.get_params())
     
    # Test the tokenizer on a piece of text
    sentences = "Работаю в провинциальном городе в магазине отделочных материалов и сантехники.Заходит к нам на днях надменная пергидролевая дева, покрытая слоем штукатурки толщиной в палец. Собирается с мыслями, напускает на себя важный вид и обращается ко мне:Дева, медленно и с видом опытного сантехника: Молодой человек, у вас ванны железные есть?Я: Нет, у нас только акрил. Металлических нет.Дева: Молодой человек, я не спрашиваю металлические, я спрашиваю железные!Я: Извините, железных тоже нет.Дева презрительно смотрит на меня, бурчит что-то себе под нос, и, виляя бедрами, уходит. Смотрим в окно. Выходит. Подходит к побитой жизнью шестерке, деловито садится на переднее сиденье, подзывает торопливо курящего поодаль водителя.Дева, возмущенно: Понабрали крестьян, металлические ванны от железных не отличают!Водитель, тяжело вздохнув, затаптывает окурок, занимает свое место, и экипаж отправляется дальше, на поиски волшебной неметаллической ванны из железа."
     
    print(tokenizer.tokenize(sentences))
    # ['Mr. James told me Dr.', 'Brown is not available today.', 'I will try tomorrow.']
     
    # View the learned abbreviations
    print(tokenizer._params.abbrev_types_)
    # set([...])

    raise
