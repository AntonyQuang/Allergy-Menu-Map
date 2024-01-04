from flask import render_template, redirect, flash, url_for, session
from flask_googlemaps import Map
from flask_login import login_required, current_user
from application.users import bp
from application.models import User, Restaurant, Report
from application.extensions import bcrypt, db
from application.managers.geolocation_manager import get_name_and_coordinates, place_id_finder, restaurant_information_finder
from .user_forms import EditUserForm, UserPasswordForm, ReportForm, UserRecommendForm
from datetime import datetime
from application.managers.price_dict import price_dict
import json

@bp.route("/recommend", methods=["GET", "POST"])
@login_required
def recommend():
    recommend_form = UserRecommendForm()
    print(recommend_form.url.data)
    if recommend_form.validate_on_submit():
        recommendation = {}
        recommendation["url"] = recommend_form.url.data
        recommendation["menu"] = recommend_form.menu.data
        recommendation["cuisines"] = recommend_form.cuisines.data
        recommendation_json = json.dumps(recommendation)
        session["recommendation"] = recommendation
        return redirect(url_for("users.add_recommendation"))
    print(recommend_form.errors.items())
    return render_template("users/recommend.html", recommend_form=recommend_form)


@bp.route("/add_recommendation/")
def add_recommendation():
    url = (session["recommendation"]["url"])
    print(url)
    name_and_coordinates = get_name_and_coordinates(url)
    print(f"name and coordinates: {name_and_coordinates}")
    place_id = place_id_finder(name_and_coordinates)
    print(f"place id: {place_id}")
    if name_and_coordinates and place_id:
        restaurant_information = restaurant_information_finder(place_id)

        confirmation_map = Map(
            identifier="view-side",
            lat=restaurant_information["latitude"],
            lng=restaurant_information["longitude"],
            markers=[(restaurant_information["latitude"], restaurant_information["longitude"])],
            style="height:300px;width:100%;margin:0;"
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
        flash(f"{restaurant_information['name']} has been submitted and will be reviewed. Thank you!", category="success")

        return render_template("users/confirmation.html", confirmation_map=confirmation_map, results=restaurant_information,
                               restaurant_id=restaurant_id)
    else:
        flash(f"Sorry, we could not find a restaurant.", category="danger")
        return redirect(url_for("users.recommend"))


@bp.route("/profile/<int:user_id>")
@login_required
def user_profile(user_id):
    session["search"] = {}
    print(current_user.id)
    if current_user.id != user_id and current_user.user_type != "Admin":
        flash("You do not have access to this page", category="danger")
        return redirect(url_for("public.home"))
    else:
        user = User.query.get_or_404(user_id)
        restaurants = user.favourites
        return render_template("users/user_profile.html", user=user, restaurants=restaurants)


@bp.route("/change-password/<int:user_id>", methods=["GET", "POST"])
@login_required
def change_password(user_id):
    if current_user.id != user_id:
        flash("You do not have access to this page", category="danger")
        return redirect(url_for("public.home"))
    user = User.query.get_or_404(user_id)
    password_form = UserPasswordForm()
    password_form.validate()
    if password_form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, password_form.old_password.data):
            hash_password = bcrypt.generate_password_hash(password_form.new_password.data)
            user.password = hash_password
            user.updated_datetime = datetime.now()
            db.session.commit()
            flash(f"Your password has been updated", category="success")
            return redirect(url_for("users.user_profile", user_id=user.id))
        else:
            flash(f"Old password is incorrect", category="danger")
            return render_template("users/edit_password.html", password_form=password_form, user=user)
    elif password_form.errors["new_password"][0] == "Passwords must match":
        flash(f"Passwords did not match", category="danger")
        return render_template("users/edit_password.html", password_form=password_form, user=user)
    return render_template("users/edit_password.html", password_form=password_form, user=user)


@bp.route("/edit-profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_profile(user_id):
    if current_user.id != user_id:
        flash("You do not have access to this page", category="danger")
        return redirect(url_for("public.home"))
    user = User.query.get_or_404(user_id)
    user_form = EditUserForm()
    if user_form.validate_on_submit():
        user.first_name = user_form.first_name.data
        user.surname = user_form.surname.data
        user.email = user_form.email.data
        user.updated_datetime = datetime.now()
        db.session.commit()
        flash(f"You details have been updated", category="success")
        return redirect(url_for("users.user_profile", user_id=user_id))
    return render_template("users/edit_profile.html", user_form=user_form, user=user)



@bp.route("/like/<int:restaurant_id>")
@bp.route("/like/<int:restaurant_id>/<search_parameters>")
@login_required
def like(restaurant_id, search_parameters=None):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    search_parameters_dict = json.loads(search_parameters.replace("'", '"'))
    if restaurant in current_user.favourites:
        return redirect(url_for("users.unlike", restaurant_id=restaurant_id, search_parameters=search_parameters))
    else:
        current_user.favourites.append(restaurant)
        db.session.commit()
        session["search"] = search_parameters_dict
        return redirect(url_for("public.search"))


@bp.route("unlike/<int:restaurant_id>")
@bp.route("unlike/<int:restaurant_id>/<search_parameters>")
@login_required
def unlike(restaurant_id, search_parameters=None):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if restaurant not in current_user.favourites:
        return redirect(url_for("users.like", restaurant_id=restaurant_id, search_parameters=search_parameters))
    else:
        current_user.favourites.remove(restaurant)
        db.session.commit()
        if search_parameters:
            search_parameters_dict = json.loads(search_parameters.replace("'",'"'))
            session["search"] = search_parameters_dict
            return redirect(url_for("public.search"))
        else:
            # If not from search then would have been from a user's profile.
            return redirect(url_for("users.user_profile", user_id=current_user.id))


@bp.route("report/<int:restaurant_id>/<search_parameters>", methods=["GET", "POST"])
@bp.route("report/<int:restaurant_id>", methods=["GET", "POST"])
@login_required
def report(restaurant_id, search_parameters=None):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    report_form = ReportForm()
    if report_form.validate_on_submit():
        report = Report(
            description=report_form.description.data,
            start_datetime=datetime.now(),
            update_datetime=datetime.now(),
            parent_user=current_user,
            parent_restaurant=restaurant,
            status="Reported"
        )
        db.session.add(report)
        db.session.commit()
        flash("Report successfully sent, thank you!" , category="success")
        if search_parameters:
            search_parameters_dict = json.loads(search_parameters.replace("'", '"'))
            session["search"] = search_parameters_dict
            return redirect(url_for("public.search"))
        else:
            return redirect(url_for("users.user_profile", user_id=current_user.id))
    if search_parameters:
        return render_template("users/report.html", report_form=report_form, restaurant=restaurant, search_parameters=search_parameters)
    else:
        return render_template("users/report.html", report_form=report_form, restaurant=restaurant)

