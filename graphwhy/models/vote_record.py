import datetime #<- will be used to set default dates on models
from .meta import Base  #<- we need to import our sqlalchemy metadata from which model classes will inherit
#from graphwhy.models.user import User  #<- we need to import our sqlalchemy metadata from which model classes will inherit
#from graphwhy.models.question_record import QuestionRecord  #<- we need to import our sqlalchemy metadata from which model classes will inherit
from sqlalchemy import (
    Column,
    Integer,
    Unicode,     #<- will provide Unicode field
    UnicodeText, #<- will provide Unicode text field
    DateTime,    #<- time abstraction field
    ForeignKey,
)
from sqlalchemy.orm import relationship

from webhelpers2.date import distance_of_time_in_words #<- human friendly dates

class VoteRecord(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    vote = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = {'extend_existing': True}
    
    question_id = Column(ForeignKey('questions.id'), nullable=False)
    question = relationship('QuestionRecord', backref='general_question_votes')

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='user_general_votes') 

    @property
    def created_in_words(self):
        return distance_of_time_in_words(self.created,
                                         datetime.datetime.utcnow())
