from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base

class AnswerOption(Base):
    """ The SQLAlchemy declarative model class for a Question's answer option Object. """
    __tablename__ = 'answer_options'
    id = Column(Integer, primary_key=True)
    option_text = Column(Text, nullable=False)
    #(for views maybe) data = Column(Text, nullable=False)
    
    question_id = Column(ForeignKey('questions.id'), nullable=False)
    question = relationship('QuestionRecord', backref='answer_options')

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_answer_options')


