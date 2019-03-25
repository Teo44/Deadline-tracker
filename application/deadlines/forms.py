from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms.fields.html5 import DateField, TimeField
from datetime import datetime

class DeadlineForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(message='Please enter a name for the deadline.')])
    date = DateField('Date', default=datetime.now())
    time = TimeField('Time')
    priority = SelectField(u"Priority", 
            # error message doesnt show up for this one
            #[validators.DataRequired(message='Please enter a date.')], 
            choices=[('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')], 
            default='2') 

    class Meta:
        csrf = False