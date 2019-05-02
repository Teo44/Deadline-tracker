from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired(message='Please enter your username.'), validators.Length(max=25, message='Name too long')])
    password = PasswordField("Password", 
                            [validators.InputRequired(message='Please enter your password'), validators.Length(max=50, message='Password too long')])

    class Meta:
        csrf = False

# Custom validator to check for whitespace in usernames
def no_whitespace(form, field):
    if " " in field.data:
        raise ValidationError("Username cannot contain whitespace")

class RegistrationForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired(message='Please enter your username.'), validators.Length(max=25, message='Name too long'), no_whitespace])
    password = PasswordField("Password", 
                            [validators.InputRequired(message='Please enter your password'), 
                                validators.Length(max=50, message='Password too long'),
                                validators.Length(min=8, message="Password must be at least 8 characters")])
    passwordagain = PasswordField("Confirm password", 
                            [validators.InputRequired(message='Please enter the password again.'), 
                                validators.Length(max=50, message="Password too long")])

    class Meta:
        csrf = False
