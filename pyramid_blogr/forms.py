from wtforms import Form, StringField, TextAreaField, validators
from wtforms import HiddenField, PasswordField

strip_filter = lambda x: x.strip() if x else None


# original blog forms
class BlogCreateForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    body = TextAreaField('Contents', [validators.Length(min=1)],
                         filters=[strip_filter])


class BlogUpdateForm(BlogCreateForm):
    id = HiddenField()

# spawned question forms
class QuestionCreateForm(Form):
    question = TextAreaField('question', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    type = TextAreaField('type', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    description = TextAreaField('description', [validators.Length(max=500)],
                         filters=[strip_filter])


class QuestionUpdateForm(QuestionCreateForm):
    id = HiddenField()


# original registrationForm
class RegistrationForm(Form):
    username = StringField('Enter a temporary username here:', [validators.Length(min=1, max=255)],
                           filters=[strip_filter], default=u'username')
    password = StringField('Password', [validators.Length(min=3)], default=u'test')
