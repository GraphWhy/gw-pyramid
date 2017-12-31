from wtforms import Form, StringField, TextAreaField, IntegerField, validators
from wtforms import HiddenField, PasswordField

strip_filter = lambda x: x.strip() if x else None

# spawned question forms
class QuestionCreateForm(Form):
    question = TextAreaField('question', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    type = TextAreaField('type', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    description = TextAreaField('description', [validators.Length(max=4000)],
                         filters=[strip_filter])


# class VoteCreateForm(Form):
#     vote = IntegerField('question', [validators.required()])
                        

class QuestionUpdateForm(QuestionCreateForm):
    id = HiddenField()


# original registrationForm
class RegistrationForm(Form):
    username = StringField('Enter a Temporary Username:', [validators.Length(min=1, max=255)],
                           filters=[strip_filter], default=u'')
    password = StringField('Password', [validators.Length(min=3)], default=u'test')
