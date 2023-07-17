from wtforms import Form, BooleanField, StringField, TextAreaField, IntegerField, validators, \
    DecimalField, SubmitField, ValidationError, URLField, SelectField, SelectMultipleField, widgets
from flask_wtf import FlaskForm


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()



class SearchForm(FlaskForm):
    location = StringField("Location", validators=[validators.DataRequired()])
    search_radius = SelectField("Search Radius", choices=[(1.0, "Within 1km"), (3.0, "Within 3km"), (5.0, "Within 5km"), (10.0, "Within 10km") ], validators=[validators.DataRequired()], coerce=float)
    price = SelectField("Price", choices=[("Any", "Any"), ("Cheap", "Cheap"), ("Medium", "Medium"), ("Expensive", "Expensive")])
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
    submit = SubmitField("Find Allergy Menus")


