from flask import render_template, redirect, url_for, session, request

from application.public import bp
from application.models import Restaurant
from .public_forms import SearchForm
from application.managers.map_manager import blank_map, search_map, home_map
from application.managers.geolocation_manager import get_user_location, boundary_box, search_for_coordinates
from application.managers.search_engine import search_engine


@bp.route("/", methods=["GET", "POST"])
def home():
    session["search"] = {}
    local_coordinates = get_user_location()
    bounding_coordinates = boundary_box(local_coordinates["latitude"], local_coordinates["longitude"], 3)
    restaurants = Restaurant.query.filter(
        Restaurant.latitude.between(bounding_coordinates["lower_latitude"], bounding_coordinates["upper_latitude"]),
        Restaurant.longitude.between(bounding_coordinates["lower_longitude"], bounding_coordinates["upper_longitude"]),
        Restaurant.status == "Confirmed"
    ).limit(10)

    if restaurants and restaurants.count() > 1:
        mymap = home_map(local_coordinates["latitude"], local_coordinates["longitude"], restaurants)

    else:
        mymap = blank_map(local_coordinates["latitude"], local_coordinates["longitude"])

    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_parameters = {
            "location": search_form.location.data,
            "search_radius": search_form.search_radius.data,
            "price": search_form.price.data,
            "cuisines": search_form.cuisines.data,
        }
        session["search"] = search_parameters
        return redirect(url_for("public.search"))
    return render_template("public/home.html", mymap=mymap, search_form=search_form)




@bp.route("/search/", methods=["GET", "POST"])
def search():
    page = request.args.get("page", 1, type=int)
    search_form = SearchForm()
    search_parameters = session["search"]
    local_coordinates = get_user_location()
    if search_form.validate_on_submit():
        search_parameters = {
            "location": search_form.location.data,
            "search_radius": search_form.search_radius.data,
            "price": search_form.price.data,
            "cuisines": search_form.cuisines.data,
        }
        session["search"] = search_parameters
        return redirect(url_for("public.search"))

    try:
        search_results = search_engine(search_parameters)
        coordinates = search_for_coordinates(search_parameters["location"])
        pagination = search_results.paginate(page=page, per_page=3, count=True)
        searchmap = search_map(coordinates["latitude"], coordinates["longitude"], pagination.items)
        if pagination.total == 0:
            blankmap = blank_map(coordinates["latitude"], coordinates["longitude"])
            return render_template("public/search.html", search_form=search_form, search_results=pagination,
                                   searchmap=blankmap, search_parameters=search_parameters)
    except KeyError:
        searchmap = blank_map(local_coordinates["latitude"], local_coordinates["longitude"])
        return render_template("public/search.html", search_form=search_form, search_results=None,
                               searchmap=searchmap, search_parameters=None)
    return render_template("public/search.html", search_form=search_form, search_results=pagination,
                                       searchmap=searchmap, search_parameters=search_parameters)
