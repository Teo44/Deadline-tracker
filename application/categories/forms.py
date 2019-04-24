from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators

class CategoryPriorityForm(FlaskForm):
    priority = SelectField("Priority",
            choices=[('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')],
            default='2')

    class Meta:
        csrf = False

class CategoryNameForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(message='Please enter a name for the category.')])

    class Meta:
        csrf = False
