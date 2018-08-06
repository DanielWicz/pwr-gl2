from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
import os

Base = declarative_base()


class User(Base):
    '''Table for storing registered users'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)  # email can be used as username
    password = Column(String, nullable=False)

    gltrait = relationship("GLTraits", back_populates='user')
    answer = relationship("Answers", back_populates='author')

    def __repr__(self):
        form = "User(id = {}, username = {})"
        return form.format(self.id, self.username)


class GLTraits(Base):
    '''Local storage for personality-related traits obtained from
    Genomelink API'''
    __tablename__ = 'gltraits'

    id = Column(Integer, primary_key=True)
    trait = Column(String)
    t_score = Column(Integer)   # Score for every trait eg. 1-5
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="gltrait")


class Questions(Base):
    '''Table for storing questions related to personality traits'''
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    trait = Column(String)
    answer = relationship("Answers", back_populates="question")


class Answers(Base):
    '''Table for storing user's answers to the questions.
    Includes self-assessment and replies from other users.'''
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer = Column(Integer)  # eg. 1-5
    user_id = Column(Integer, ForeignKey('users.id'))
    question = relationship("Questions", back_populates="answer")
    author = relationship("User", back_populates="answer")


if __name__ == '__main__':

    db_filename = 'main.db'
    if os.access(db_filename, os.F_OK):
        os.remove(db_filename)
    engine = create_engine('sqlite:///{}'.format(db_filename))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    user = User()
    user.id = 0
    user.username = 'Janusz@example.com'
    user.password = '12345'

    session.add(user)
    session.commit()

    users = session.query(User).all()

    for i in users:
        print(i.id, i.username)
        print(i)

    session.close()