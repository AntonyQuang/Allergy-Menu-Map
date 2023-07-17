from flask_googlemaps import Map


def home_map(local_latitude, local_longitude, restaurants):
    map = Map(
            identifier="default-map",
            lat=float(local_latitude),
            lng=float(local_longitude),
            markers=[
                {
                    "lat": float(restaurant.latitude),
                    "lng": float(restaurant.longitude),
                    "infobox": f"<div class='card-title'><a href='{restaurant.maps_url}' target='_blank'><h6>{restaurant.name}</h3></a></div> "
                               f"<div class='card-body py-2'>{restaurant.address}</div>"
                               f"<a class='btn-sm btn btn-outline-secondary' href='{restaurant.menu}' target='_blank'>"
                               f"Allergy Menu"
                               f"</a>",
                }
                for restaurant in restaurants],
            fit_markers_to_bounds=True,
            style="height:600px;width:100%;margin:0;"
        )
    return map


def blank_map(local_latitude, local_longitude):
    map = Map(
            identifier="default-map",
            lat=float(local_latitude),
            lng=float(local_longitude),
            fit_markers_to_bounds=False,
            style="height:600px;width:100%;margin:0;"
        )
    return map


def search_map(target_latitude, target_longitude, search_results):
    map = Map(
        identifier="search-map",
        lat=target_latitude,
        lng=target_longitude,
        markers=[
            {
                "lat": float(restaurant.latitude),
                "lng": float(restaurant.longitude),
                "infobox": f"<div class='card-title'><a href='{restaurant.maps_url}' target='_blank'><h6>{restaurant.name}</h3></a></div> "
                           f"<div class='card-body py-2'>{restaurant.address}</div>"
                           f"<a class='btn-sm btn btn-outline-secondary' href='{restaurant.menu}' target='_blank'>"
                           f"Allergy Menu"
                           f"</a>"
            }
            for restaurant in search_results],
        fit_markers_to_bounds=True,
        style="height:600px;width:100%;margin:0;",
    )
    return map

