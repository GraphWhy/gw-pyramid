from wtforms import Form, StringField, TextAreaField, IntegerField, validators
from wtforms import HiddenField, PasswordField, FieldList, FormField

# used to remove all whitespace from beginning and end of question
strip_filter = lambda x: x.strip() if x else None


class QuestionOptionForm(Form):
    question_option = TextAreaField('Answer Options', [validators.Length(min=1, max=255)], filters=[strip_filter])  

# spawned question forms
class QuestionCreateForm(Form):
    question = TextAreaField('Daily Prompt :  ', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    color = TextAreaField('Key Color [#111111] :', [validators.Length(min=6, max=7)], filters=[strip_filter])
    type = TextAreaField('Subject', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    description = TextAreaField('Context', [validators.Length(max=500)],
                         filters=[strip_filter])
    question_option = FieldList(FormField(QuestionOptionForm), min_entries=2, max_entries=101)  

# class VoteCreateForm(Form):
#     vote = IntegerField('question', [validators.required()])



class QuestionUpdateForm(QuestionCreateForm):
    id = HiddenField()


# original registrationForm
class RegistrationForm(Form):
    username = StringField('Username:', [validators.Length(min=1, max=255)],
                           filters=[strip_filter], default=u'')
    password = StringField('Password:', [validators.Length(min=3)], default=u'test')
