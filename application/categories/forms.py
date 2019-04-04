from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators

class CategoryPriorityForm(FlaskForm):
    priority = SelectField("Priority",
            choices=[('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')],
            default='2')

    class Meta:
        csrf = False

