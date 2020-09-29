from wtforms import Form, HiddenField, StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired


class QuestionForm(Form):
    category = SelectField("Category", choices=[], coerce=int)
    title = StringField("Title", validators=[InputRequired()])
    description = TextAreaField("Content", validators=[InputRequired()])


class QuestionEditForm(Form):
    category = SelectField("Category", choices=[], coerce=int)
    title = StringField(validators=[InputRequired()])
    description = TextAreaField(validators=[InputRequired()])


class AnswerForm(Form):
    content = TextAreaField("Content", validators=[InputRequired()])


class AnswerEditForm(Form):
    content = TextAreaField(validators=[InputRequired()])


class AnswerLikesForm(Form):
    answer_id = HiddenField()


class QuestionLikesForm(Form):
    question_id = HiddenField()


class AcceptedAnswerForm(Form):
    answer_id = HiddenField()
