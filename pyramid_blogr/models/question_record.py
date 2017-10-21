import datetime #<- will be used to set default dates on models
from pyramid_blogr.models.meta import Base  #<- we need to import our sqlalchemy metadata from which model classes will inherit
from pyramid_blogr.models.user import User  #<- we need to import our sqlalchemy metadata from which model classes will inherit
from sqlalchemy import (
    Column,
    Integer,
    Unicode,     #<- will provide Unicode field
    UnicodeText, #<- will provide Unicode text field
    DateTime,    #<- time abstraction field
    ForeignKey,
)
from webhelpers2.text import urlify #<- will generate slugs
from webhelpers2.date import distance_of_time_in_words #<- human friendly dates

class QuestionRecord(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    question = Column(Unicode(255), nullable=False)
    description = Column(UnicodeText, default=u'No description')
    type = Column(Unicode(255), nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = {'extend_existing': True}

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return distance_of_time_in_words(self.created,
                                         datetime.datetime.utcnow())
