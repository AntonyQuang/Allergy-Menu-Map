from wtforms import StringField, PasswordField, validators, \
    DecimalField, SubmitField, ValidationError, EmailField, SelectField, SelectMultipleField, widgets, TextAreaField
from flask_wtf import FlaskForm


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()



class RestaurantForm(FlaskForm):
    name = StringField("Name", [validators.length(max=150), validators.DataRequired()])
    latitude = DecimalField("Latitude", [
        validators.NumberRange(min=-90, max=90, message="Latitude needs to be between -90 and 90")])
    longitude = DecimalField("Longitude", [
        validators.NumberRange(min=-180, max=180, message="Longitude needs to be between -180 and 180")])
    price = SelectField("Price", choices=[("Cheap", "Cheap"), ("Medium", "Medium"), ("Expensive", "Expensive")])
    website = StringField("Website", [validators.DataRequired()])
    menu = StringField("Link to Allergy Menu", [validators.DataRequired()])
    phone = StringField("Contact Number")
    address = StringField("Address", [validators.DataRequired()])
    status = SelectField("Status", choices=[("Proposed", "Proposed"), ("Confirmed", "Confirmed"), ("Closed", "Closed")],
                         validators=[validators.DataRequired()])
    maps_url = StringField("Google Maps URL", [validators.DataRequired()])
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
                                            ("Japanese", "Japanese"),
                                            ("Korean", "Korean"),
                                            ("Mexican", "Mexican"),
                                            ("Mediterranean", "Mediterranean"),
                                            ("Italian", "Italian"),
                                            ("Seafood", "Seafood"),
                                            ("Thai", "Thai"),
                                            ("Turkish", "Turkish"),
                                            ("Vegetarian", "Vegetarian"),
                                            ("Vegan", "Vegan"),
                                            ("Halal", "Halal"),
                                            ]
                                   )

    submit = SubmitField("Submit")


class AdminEditUserForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=30), validators.DataRequired()])
    first_name = StringField("First Name", [validators.Length(min=3, max=50), validators.DataRequired()])
    surname = StringField("Surname", [validators.Length(min=3, max=50), validators.DataRequired()])
    email = EmailField("Email Address", [validators.Length(min=6, max=180), validators.Email()])
    user_type = SelectField("Status",
                            choices=[("User", "User"), ("Admin", "Admin"), ("Banned", "Banned")])
    update = SubmitField("Update User")


class AdminPasswordForm(FlaskForm):
    new_password = PasswordField("New Password", [validators.Length(min=3, max=180), validators.DataRequired(),
                                                  validators.EqualTo("confirm_password",
                                                                     message="Passwords must match")])
    confirm_password = PasswordField("Confirm Password", [validators.DataRequired()])
    update = SubmitField("Update Password")


class AdminReportForm(FlaskForm):
    description = TextAreaField("Report Description", [validators.Length(max=500), validators.DataRequired()])
    status = SelectField("Report Status", choices=[("Reported", "Reported"), ("In progress", "In progress"),
                                                   ("Closed", "Closed")], validators=[validators.DataRequired()])
    update = SubmitField("Update Report")

