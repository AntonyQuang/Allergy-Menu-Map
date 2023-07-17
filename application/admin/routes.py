from flask import render_template, redirect, url_for, flash
from flask_googlemaps import Map
from flask_login import login_user, login_required, current_user, logout_user
from application.admin import bp
from application.models import Restaurant, User, Report
from .admin_forms import RestaurantForm, AdminPasswordForm, AdminEditUserForm, AdminReportForm
from datetime import datetime
from application.extensions import db, bcrypt




# --------------------- Restaurant function --------------------- #

@bp.route("/database/restaurants")
@login_required
def restaurant_database():
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for('public.home'))
    restaurants = Restaurant.query.all()
    return render_template("admin/restaurant_database.html", restaurants=restaurants)

@bp.route("/database/restaurants/user/<int:user_id>")
@login_required
def user_favourites_database(user_id):
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for('public.home'))
    user=User.query.get_or_404(user_id)
    restaurants = user.favourites
    return render_template("admin/restaurant_database.html", restaurants=restaurants, user=user)


@bp.route("/database/proposed-restaurants")
@login_required
def proposed_restaurant_database():
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for('public.home'))
    restaurants = Restaurant.query.filter_by(status="Proposed").all()
    return render_template("admin/restaurant_database.html", restaurants=restaurants)



@bp.route("/edit/restaurant/<int:restaurant_id>", methods=["GET", "POST"])
@login_required
def edit_restaurant(restaurant_id):
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for('public.home'))
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    restaurant_form = RestaurantForm()
    if restaurant_form.validate_on_submit():
        restaurant.name = restaurant_form.name.data
        restaurant.latitude = restaurant_form.latitude.data
        restaurant.longitude = restaurant_form.longitude.data
        restaurant.price = restaurant_form.price.data
        restaurant.website = restaurant_form.website.data
        restaurant.menu = restaurant_form.menu.data
        restaurant.status = restaurant_form.status.data
        restaurant.phone = restaurant_form.phone.data
        restaurant.update_datetime = datetime.now()
        restaurant.address = restaurant_form.address.data
        restaurant.maps_url = restaurant_form.maps_url.data
        restaurant.cuisines = restaurant_form.cuisines.data
        db.session.commit()
        flash("Changes have been made", category="success")
        return redirect(url_for("admin.restaurant_database"))
    restaurant_form.price.default = restaurant.price
    restaurant_form.status.default = restaurant.status
    restaurant_form.cuisines.default = restaurant.cuisines
    restaurant_form.process()
    print(restaurant_form.errors)
    return render_template("admin/edit_restaurant.html", restaurant_form=restaurant_form, restaurant=restaurant)


@bp.route("/add_restaurant", methods=["GET", "POST"])
@login_required
def add_restaurant():
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for('public.home'))
    restaurant_form = RestaurantForm()
    if restaurant_form.validate_on_submit():
        restaurant = Restaurant(
            name=restaurant_form.name.data,
            latitude=restaurant_form.latitude.data,
            longitude=restaurant_form.longitude.data,
            price=restaurant_form.price.data,
            website=restaurant_form.website.data,
            menu=restaurant_form.menu.data,
            status=restaurant_form.status.data,
            phone=restaurant_form.phone.data,
            start_datetime=datetime.now(),
            update_datetime=datetime.now(),
            address=restaurant_form.address.data,
            maps_url=restaurant_form.maps_url.data,
            cuisines=restaurant_form.cuisines.data)
        db.session.add(restaurant)
        db.session.commit()
        flash("Changes have been made", category="success")
        return redirect(url_for("admin.restaurant_database"))
    print(restaurant_form.errors)
    return render_template("admin/add_restaurant.html", restaurant_form=restaurant_form)


# -------------- User function -------------------- #


@bp.route("/database/users")
@login_required
def user_database():
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for('public.home'))
    users = User.query.all()
    return render_template("admin/user_database.html", users=users)


@bp.route("/edit/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for('public.home'))
    user_form = AdminEditUserForm()
    user = User.query.get_or_404(user_id)
    if user_form.validate_on_submit():
        user.username = user_form.username.data
        user.first_name = user_form.first_name.data
        user.surname = user_form.surname.data
        user.email = user_form.email.data
        user.user_type = user_form.user_type.data
        user.updated_datetime = datetime.now()
        db.session.commit()
        flash(f"User details for {user.username} has been completed", category="success")
        return redirect(url_for("admin.user_database"))
    user_form.user_type.default = user.user_type
    user_form.process()
    print(user_form.errors)
    return render_template("admin/edit_user.html", user_form=user_form, user=user)


@bp.route("/edit/users/password/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_password(user_id):
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for('public.home'))
    password_form = AdminPasswordForm()
    user = User.query.get_or_404(user_id)
    password_form.validate()
    if password_form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(password_form.new_password.data)
        user.password = hash_password
        user.updated_datetime = datetime.now()
        db.session.commit()
        flash(f"Password for {user.username} successfully updated", category="success")
        return redirect(url_for("admin.user_database"))
    elif password_form.errors["new_password"][0] == "Passwords must match":
        flash(f"Passwords did not match", category="danger")
        return render_template("admin/edit_password.html",
                               password_form=password_form, user=user)
    return render_template("admin/edit_password.html", user=user,
                           password_form=password_form)



# ------------------ Report functions ------------------ #

@bp.route("/reports/<open_reports>")
@bp.route("/reports/<int:restaurant_id>")
@bp.route("/reports")
@login_required
def report_database(restaurant_id=None, open_reports=None):
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for("public.home"))
    if restaurant_id:
        reports = Report.query.filter_by(parent_restaurant_id=restaurant_id)
    elif open_reports:
        reports = Report.query.filter(Report.status != "Closed")
    else:
        reports = Report.query.all()
    return render_template("admin/report_database.html", reports=reports)


@bp.route("edit/report/<int:report_id>", methods=["GET", "POST"])
@login_required
def edit_report(report_id, previous_page=None):
    if current_user.user_type != "Admin":
        flash("You do not have access to this page.")
        return redirect(url_for("public.home"))
    report = Report.query.filter_by(id=report_id).first()
    report_form = AdminReportForm()
    if report_form.validate_on_submit():
        report.description = report_form.description.data
        report.status = report_form.status.data
        report.update_datetime = datetime.now()
        db.session.commit()
        return redirect(url_for("admin.report_database"))
    report_form.status.default = report.status
    report_form.description.default = report.description
    report_form.process()
    return render_template("admin/edit_report.html", report=report, report_form=report_form)

