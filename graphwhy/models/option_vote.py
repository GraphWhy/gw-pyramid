import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship

from .meta import Base

class OptionVote(Base):
    """ The SQLAlchemy declarative model class for a Question's answer option Object. """
    __tablename__ = 'option_votes'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
 
    option_id = Column(ForeignKey('answer_options.id'), nullable=False)
    option = relationship('AnswerOption', backref='votes')

    question_id = Column(ForeignKey('questions.id'), nullable=False)
    question = relationship('QuestionRecord', backref='question_votes')

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='user_votes')


