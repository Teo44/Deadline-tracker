from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms.fields.html5 import DateField, TimeField
from datetime import datetime

class DeadlineForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(message='Please enter a name for the deadline.')])
    date = DateField('Date', 
            [validators.InputRequired(message='Please enter a date')], 
            default=datetime.now())
    time = TimeField('Time')
    priority = SelectField(u"Priority", 
            #[validators.DataRequired(message='Please enter a date.')], 
            choices=[('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')], 
            default='2') 
    # TODO: validators for category? It can be left empty though, maybe none?
    category = StringField("Category")

    class Meta:
        csrf = False

class DeadlineCategoryFilterForm(FlaskForm):
    category = SelectField("Category", choices=[], coerce=int)
    priority = SelectField("Priority",
                            choices=[('0', '-'), ('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')], 
                            default='0')

    class Meta:
        csrf = False

