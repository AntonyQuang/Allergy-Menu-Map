import flask
from flask import render_template, redirect, session, url_for, flash, request
from flask_login import login_user, login_required, current_user, logout_user, login_manager
from application.extensions import login_manager, bcrypt, db
from flask import render_template
from application.models import User
from .login_functionality_forms import LoginForm, RegistrationForm
from datetime import datetime
from config import Config
from application.login_functionality import bp


@bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", category="warning")
        return redirect(url_for("public.home"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data.lower()).first()
        if user.user_type == "Banned":
            flash("I'm sorry, but you have been banned from being a member this website", category="danger")
            return redirect(url_for("public.home"))
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f"Hi {current_user.first_name}, you have logged in", category="success")
            print("Log in success")
            return redirect(next_page or url_for('public.home'))
        else:
            flash("Log in details are incorrect", category="danger")
            return redirect(url_for("login_functionality.login"))
    return render_template("login_functionality/login.html", login_form=login_form)





@bp.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        username_check = User.query.filter_by(username=register_form.username.data.lower()).first()
        if username_check:
            flash("Username has already been taken", category="warning")
            return redirect(url_for("login_functionality.register"))
        email_check = User.query.filter_by(email=register_form.email.data.lower()).first()
        if email_check:
            flash("Email is already associated with another account", category="warning")
            return redirect(url_for("login_functionality.register"))
        hash_password = bcrypt.generate_password_hash(register_form.password.data)

        user = User(username=register_form.username.data.lower(),
                    first_name=register_form.first_name.data.title(),
                    surname=register_form.surname.data.title(),
                    email=register_form.email.data.lower(),
                    password=hash_password,
                    start_datetime=datetime.now(),
                    updated_datetime=datetime.now(),
                    user_type="Pending Verification")
        db.session.add(user)
        db.session.commit()
        registered_user = User.query.filter_by(username=register_form.username.data).first()
        if registered_user.id == 1:
            registered_user.user_type = "Admin"
            db.session.commit()
        flash(f"Hi {register_form.first_name.data}, thank you for registering", "success")
        return redirect(url_for("login_functionality.login"))
    return render_template("login_functionality/register.html", register_form=register_form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.home"))


@bp.route("/demo_user_login")
def demo_user_login():
    if current_user.is_authenticated:
        flash("You are already logged in", category="warning")
        return redirect(url_for("public.home"))
    user = User.query.filter_by(email=Config.demo_user_email.lower()).first()
    login_user(user)
    next_page = request.args.get('next')
    flash(f"Hi {current_user.first_name}, you have logged in", category="success")
    print("Log in success")
    return redirect(next_page or url_for('public.home'))


@bp.route("/demo_admin_login")
def demo_admin_login():
    if current_user.is_authenticated:
        flash("You are already logged in", category="warning")
        return redirect(url_for("public.home"))
    user = User.query.filter_by(email=Config.demo_admin_email.lower()).first()
    login_user(user)
    next_page = request.args.get('next')
    flash(f"Hi {current_user.first_name}, you have logged in", category="success")
    print("Log in success")
    return redirect(next_page or url_for('public.home'))

