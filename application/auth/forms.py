from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired(message='Please enter your username.')])
    password = PasswordField("Password", 
                            [validators.InputRequired(message='Please enter your password')])

    class Meta:
        csrf = False

def no_whitespace(form, field):
    if " " in field.data:
        raise ValidationError("Username cannot contain whitespace")

class RegistrationForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired(message='Please enter a username.'), 
                                        no_whitespace])
    password = PasswordField("Password", [validators.InputRequired(message='Please enter a password'), validators.Length(min=8, message='Password must be at least 8 characters long'), validators.EqualTo('passwordagain', message='Passwords did not match')])
    passwordagain = PasswordField("Confirm password", [validators.InputRequired(message='Please enter the password again.')])

    class Meta:
        csrf = False
