from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms.fields.html5 import DateField, TimeField, DateTimeField
from datetime import datetime

class DeadlineForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(message='Please enter a name for the deadline.')])
    date = DateField('Date', 
            [validators.InputRequired(message='Please enter a date')], 
                default=datetime.now())
    hour_selection = []
    for x in range(24):
        hour_selection.append((x, format(x, '02d')))
    hour = SelectField("Time", choices=hour_selection, coerce=int)
    minute_selection = []
    for x in range(60):
        minute_selection.append((x, format(x, '02d')))
    minute = SelectField("Time_minute", choices=minute_selection, coerce=int)

    priority = SelectField(u"Priority", 
            #[validators.DataRequired(message='Please enter a date.')], 
            choices=[('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')], 
            default='2') 
    # TODO: validators for category? It can be left empty though, maybe none?
    category = StringField("Category")


    class Meta:
        csrf = False

class DeadlineCategoryFilterForm(FlaskForm):
    date_order = SelectField("Date_order", choices=[(0, '-'), (1, 'Descending'), (2, 'Ascending')])
    category = SelectField("Category", choices=[], coerce=int)
    priority = SelectField("Priority",
                            choices=[('0', '-'), ('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')], 
                            default='0')

    class Meta:
        csrf = False

class DeadlineNameForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(message='Please enter a name for the deadline.')])

    class Meta:
        csrf = False
