from application.models import Restaurant
from application.managers.geolocation_manager import search_for_coordinates, boundary_box


def search_engine(search_parameters):
    coordinates = search_for_coordinates(search_parameters["location"])
    if not coordinates:
        return None

    bounding_coordinates = boundary_box(coordinates["latitude"], coordinates["longitude"],
                                            search_parameters["search_radius"])

    # Different queries based on both cuisines and prices either being on or off:

    # Cuisines and Price
    if search_parameters["cuisines"] and search_parameters["price"] != "Any":
        queries = []
        for cuisine in search_parameters["cuisines"]:
            query = Restaurant.query.filter(
                Restaurant.latitude.between(bounding_coordinates["lower_latitude"],
                                            bounding_coordinates["upper_latitude"]),
                Restaurant.longitude.between(bounding_coordinates["lower_longitude"],
                                             bounding_coordinates["upper_longitude"]),
                Restaurant.status == "Confirmed",
                Restaurant.price == search_parameters["price"],
                Restaurant.cuisines.contains(cuisine)
            )
            queries.append(query)
        restaurants = queries[0].union(*queries[1:])
        return restaurants

    # No cuisines and no price
    if not search_parameters["cuisines"] and search_parameters["price"] == "Any":
        restaurants = Restaurant.query.filter(
            Restaurant.latitude.between(bounding_coordinates["lower_latitude"],
                                        bounding_coordinates["upper_latitude"]),
            Restaurant.longitude.between(bounding_coordinates["lower_longitude"],
                                         bounding_coordinates["upper_longitude"]),
            Restaurant.status == "Confirmed",
        )
        return restaurants
    # No cuisine and Price
    if not search_parameters["cuisines"] and search_parameters["price"]:
        restaurants = Restaurant.query.filter(
            Restaurant.latitude.between(bounding_coordinates["lower_latitude"],
                                        bounding_coordinates["upper_latitude"]),
            Restaurant.longitude.between(bounding_coordinates["lower_longitude"],
                                         bounding_coordinates["upper_longitude"]),
            Restaurant.status == "Confirmed",
            Restaurant.price == search_parameters["price"]
        )
        return restaurants
    # Cuisine and no price

    if search_parameters["cuisines"] and search_parameters["price"] == "Any":
        queries = []
        for cuisine in search_parameters["cuisines"]:
            query = Restaurant.query.filter(
                Restaurant.latitude.between(bounding_coordinates["lower_latitude"],
                                            bounding_coordinates["upper_latitude"]),
                Restaurant.longitude.between(bounding_coordinates["lower_longitude"],
                                             bounding_coordinates["upper_longitude"]),
                Restaurant.status == "Confirmed",
                Restaurant.cuisines.contains(cuisine)
            )
            queries.append(query)
        restaurants = queries[0].union(*queries[1:])
        return restaurants