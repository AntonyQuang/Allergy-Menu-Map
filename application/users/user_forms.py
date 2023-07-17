from wtforms import StringField, PasswordField, IntegerField, validators, \
    DecimalField, SubmitField, ValidationError, EmailField, SelectField, SelectMultipleField, TextAreaField, URLField, widgets
from flask_wtf import FlaskForm


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()


class EditUserForm(FlaskForm):
    first_name = StringField("First Name", [validators.Length(min=3, max=50), validators.DataRequired()])
    surname = StringField("Surname", [validators.Length(min=3, max=50), validators.DataRequired()])
    email = EmailField("Email Address", [validators.Length(min=6, max=180), validators.Email()])
    update = SubmitField("Update Details")


class UserPasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", [validators.DataRequired()])
    new_password = PasswordField("New Password", [validators.Length(min=3, max=180), validators.DataRequired(),
                                                  validators.EqualTo("confirm_password",
                                                                     message="Passwords must match")])
    confirm_password = PasswordField("Confirm Password")
    update = SubmitField("Update Password")


class ReportForm(FlaskForm):
    description = TextAreaField("Describe what's wrong", [validators.Length(max=500), validators.DataRequired()])
    submit = SubmitField("Submit Report")


class UserRecommendForm(FlaskForm):
    url = URLField("Google Maps Link",
                   validators=[validators.DataRequired()])

    menu = URLField("Link to Allergy Menu", validators=[validators.DataRequired()])

    cuisines = MultiCheckboxField("Cuisines",
                                  choices=[("African", "African"),
                                           ("American", "American"),
                                           ("Asian", "Asian"),
                                           ("BBQ", "BBQ"),
                                           ("British", "British"),
                                           ("Brunch", "Brunch"),
                                           ("Burger", "Burger"),
                                           ("Caribbean", "Caribbean"),
                                           ("Chicken", "Chicken"),
                                           ("Chinese", "Chinese"),
                                           ("Indian", "Indian"),
                                           ("Italian", "Italian"),
                                           ("Japanese", "Japanese"),
                                           ("Korean", "Korean"),
                                           ("Mexican", "Mexican"),
                                           ("Mediterranean", "Mediterranean"),
                                           ("Seafood", "Seafood"),
                                           ("Thai", "Thai"),
                                           ("Turkish", "Turkish"),
                                           ("Vegetarian", "Vegetarian"),
                                           ("Vegan", "Vegan"),
                                           ("Halal", "Halal"),
                                           ],

                                  )
    submit = SubmitField("Recommend")