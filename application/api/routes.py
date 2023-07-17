from flask import render_template, flash, redirect, url_for, session
from flask_googlemaps import Map
from flask_login import login_required
from application.api import bp
from application.models import Restaurant
from application.extensions import db
from datetime import datetime
import json
from application.managers.geolocation_manager import get_name_and_coordinates, restaurant_information_finder, place_id_finder
from application.managers.price_dict import price_dict

@bp.route("/")
def explanation():
    return render_template("public/home.html", mymap=mymap, sndmap=sndmap)


@bp.route("/search")
def search():
    pass


@bp.route("/recommend", methods=["GET", "POST"])
@login_required
def recommend():
    recommend_form = PublicRecommendForm()
    print(recommend_form)
    if recommend_form.validate_on_submit():
        recommendation = {}
        recommendation["url"] = recommend_form.url.data
        recommendation["menu"] = recommend_form.menu.data
        recommendation["cuisines"] = recommend_form.cuisines.data
        recommendation_json = json.dumps(recommendation)
        session["recommendation"] = recommendation
        return redirect(url_for("public.add_recommendation"))
    print(recommend_form.errors.items())
    return render_template("public/recommend.html", recommend_form=recommend_form)


@bp.route("/add_recommendation/")
def add_recommendation():
    url = (session["recommendation"]["url"])
    print(url)
    name_and_coordinates = get_name_and_coordinates(url)
    place_id = place_id_finder(name_and_coordinates)
    if name_and_coordinates and place_id:
        restaurant_information = restaurant_information_finder(place_id)

        confirmation_map = Map(
            identifier="view-side",
            lat=restaurant_information["latitude"],
            lng=restaurant_information["longitude"],
            markers=[(restaurant_information["latitude"], restaurant_information["longitude"])],
            style="height:300px;width:600px;margin:0;"
        )

        restaurant_information["maps_url"] = session["recommendation"]["url"]
        restaurant_information["cuisines"] = session["recommendation"]["cuisines"]
        restaurant_information["menu"] = session["recommendation"]["menu"]
        restaurant_information["price"] = price_dict[restaurant_information["price"]]


        restaurant = Restaurant(
            name=restaurant_information["name"],
            latitude=restaurant_information["latitude"],
            longitude=restaurant_information["longitude"],
            price=restaurant_information["price"],
            website=restaurant_information["website"],
            menu=session["recommendation"]["menu"],
            phone=restaurant_information["phone"],
            start_datetime=datetime.now(),
            update_datetime=datetime.now(),
            address=restaurant_information["address"],
            maps_url=restaurant_information["maps_url"],
            cuisines=restaurant_information["cuisines"],
        )

        db.session.add(restaurant)
        db.session.commit()

        restaurant_in_db = Restaurant.query.filter_by(maps_url=restaurant.maps_url).first()
        restaurant_id = restaurant_in_db.id
        flash(f"{restaurant_information['name']} has been submitted and will be reviewed. Thank you!")

        return render_template("public/confirmation.html", testmap=confirmation_map, results=restaurant_information, restaurant_id=restaurant_id)
    else:
        flash(f"Sorry, we could not find a restaurant.", category="danger")
        return redirect(url_for("public.recommend"))


@bp.route("/report/<int:id>")
@login_required
def report(restaurant_id):
    pass


@bp.route("/test")
def test():
    url = "https://goo.gl/maps/rEAU9QnVzAj2oYPh6"
    name_and_coordinates = get_name_and_coordinates(url)
    if name_and_coordinates:
        place_id = place_id_finder(name_and_coordinates)
        restaurant_information = restaurant_information_finder(place_id)

        testmap = Map(
            identifier="view-side",
            lat=restaurant_information["latitude"],
            lng=restaurant_information["longitude"],
            markers=[(restaurant_information["latitude"], restaurant_information["longitude"])],
            style="height:300px;width:600px;margin:0;"
        )

        print(restaurant_information)

        return render_template("public/confirmation.html", testmap=testmap, results=restaurant_information)
