from wtforms import Form, BooleanField, StringField, PasswordField, TextAreaField, IntegerField, validators, \
    DecimalField, SubmitField, ValidationError, EmailField
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=30), validators.DataRequired()])
    first_name = StringField("First Name", [validators.Length(min=3, max=50), validators.DataRequired()])
    surname = StringField("Surname", [validators.Length(min=3, max=50), validators.DataRequired()])
    email = EmailField("Email Address", [validators.Length(min=6, max=180), validators.Email()])
    password = PasswordField("Password", [validators.Length(min=3, max=180), validators.DataRequired(),
                                          validators.EqualTo("confirm_password", message="Passwords must match")])
    confirm_password = PasswordField("Repeat Password")
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
    ])
    submit = SubmitField("Log In")