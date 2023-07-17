from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from application.extensions import login_manager, db


# Secondary table to join User and Restaurant



user_restaurant = db.Table("user_restaurant",
                           db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                           db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurants.id'))
                           )


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(), default="User", nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    updated_datetime = db.Column(db.DateTime)
    # Relationships
    # Many to many with Restaurant
    favourites = db.relationship("Restaurant", secondary=user_restaurant, backref="fans")
    # One to many with Reports
    reports = db.relationship("Report", back_populates="parent_user")

    def __repr__(self):
        return f"User Class Object: {self.username}"


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


# Create json type decorator for restaurants
class JsonEncodedDict(db.TypeDecorator):

    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.loads(value)


class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    latitude = db.Column(db.Numeric, nullable=False)
    longitude = db.Column(db.Numeric, nullable=False)
    price = db.Column(db.String(3), nullable=False)
    website = db.Column(db.String(), nullable=False)
    menu = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(30), default="Proposed", unique=False, nullable=False)
    phone = db.Column(db.String())
    start_datetime = db.Column(db.DateTime, nullable=False)
    update_datetime = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(250), unique=False, nullable=False)
    maps_url = db.Column(db.String(), nullable=False)

    # Cuisines
    cuisines = db.Column(JsonEncodedDict)

    # Relationships
    # One to many with Reports
    reports = db.relationship("Report", back_populates="parent_restaurant")

    def __repr__(self):
        return f"Restaurant Class Object: {self.name} at ({self.latitude}, {self.longitude})"


class Report(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140), unique=False, nullable=False)
    status = db.Column(db.String(), default="Reported")
    start_datetime = db.Column(db.DateTime, nullable=False)
    update_datetime = db.Column(db.DateTime, nullable=False)
    # Relationships
    # Many to one with User and Restaurant
    parent_user = db.relationship("User", back_populates="reports")
    parent_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_restaurant = db.relationship("Restaurant", back_populates="reports")
    parent_restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))

    def __repr__(self):
        return f"Report Class Object: Made by {self.parent_user.username} about {self.parent_restaurant.name}"


