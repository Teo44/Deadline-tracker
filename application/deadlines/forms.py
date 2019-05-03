from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, ValidationError, BooleanField
from wtforms.fields.html5 import DateField, TimeField, DateTimeField
from datetime import datetime

def not_empty(form, field):
    if field.data.isspace():
        raise ValidationError("Deadline name cannot be blank")

class DeadlineForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(message='Please enter a name for the deadline.'), validators.Length(max=25, message='Name too long'), not_empty])
    date = DateField('Date', 
            [validators.InputRequired(message='Please enter a date')], 
                default=datetime.now())

    # Time selection fields, because html doesn't have 24h time selection (?!)
    hour_selection = []
    for x in range(24):
        hour_selection.append((x, format(x, '02d')))
    hour = SelectField("Time", choices=hour_selection, coerce=int)
    minute_selection = []
    for x in range(60):
        minute_selection.append((x, format(x, '02d')))
    minute = SelectField("Time_minute", choices=minute_selection, coerce=int)

    priority = SelectField(u"Priority", 
            choices=[('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')], 
            default='2') 
    category = StringField("Category", [validators.Length(max=25, message='Category name too long')])

    class Meta:
        csrf = False

class DeadlineCategoryFilterForm(FlaskForm):
    date_order = SelectField("Date_order", choices=[(0, '-'), (1, 'Descending'), (2, 'Ascending')])
    category = SelectField("Category", choices=[], coerce=int)
    priority = SelectField("Priority",
                            choices=[('0', '-'), ('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')], 
                            default='0')

    categorypriority = SelectField("Categorypriority",
                            choices=[('0', '-'), ('1', 'Optional'), ('2', 'Normal'), ('3', 'Urgent')], 
                            default='0')
    hide_old_deadlines = BooleanField()

    page = SelectField("Page", choices=[], coerce=int)

    class Meta:
        csrf = False

class DeadlineNameForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(message='Please enter a name for the deadline.'), validators.Length(max=25, message='Name too long')])

    class Meta:
        csrf = False

class DeadlineCategoryForm(FlaskForm):
    category = StringField('Category', [validators.InputRequired(message='Please enter a category.'), validators.Length(max=25, message='Category name too long')])

    class Meta:
        csrf = False

