import requests
from config import Config
import json
from flask import request
import math


def get_name_and_coordinates(url):
    if url[0:24] != "https://maps.app.goo.gl/":
        return False
    response = requests.get(url, headers={'User-Agent': 'Google Chrome'})
    destination_url = response.history[-1].url
    print(f"Destination url is: {destination_url}")
    # destination_url will come in the form:
    # https://www.google.com/maps/place/McDonald's/@51.4196017,-0.2064303,16.5z/data=....
    destination_url_list = destination_url.split("/")

    # Turning /@51.4196017,-0.2064303,16.5z/ into a list
    lat_lon = destination_url_list[6].strip("@z").split(",")

    name_and_coordinates = {}
    name_and_coordinates["name"] = destination_url_list[5]
    name_and_coordinates["latitude"] = lat_lon[0]
    name_and_coordinates["longitude"] = lat_lon[1]
    print(f"Output is {name_and_coordinates}")
    return name_and_coordinates


def place_id_finder(name_and_coordinates):
    if not name_and_coordinates:
        return False
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    # print(name_and_coordinates)
    query_name = name_and_coordinates["name"].replace("+", "%20")
    # print(query_name)
    payload = {
        "query": query_name,
        "location": f"{name_and_coordinates['latitude']}%2C{name_and_coordinates['longitude']}",
        "radius": "200",
        "key": Config.GOOGLE_API_KEY
    }
    # print(payload["location"])
    # response = requests.get(endpoint, params=payload, headers={'User-Agent': 'Google Chrome'})
    print(
        f"{endpoint}?query={payload['query']}&location={payload['location']}&radius={payload['radius']}&key={payload['key']}")
    response = requests.get(
        f"{endpoint}?query={payload['query']}&location={payload['location']}&radius={payload['radius']}&key={payload['key']}",
        headers={'User-Agent': 'Google Chrome'})
    response_dict = json.loads(response.text)
    print(f"Response dict: {response_dict}")
    if response_dict["status"] == "ZERO_RESULTS":
        return False
    else:
        place_id = response_dict["results"][0]["place_id"]
        return place_id


def restaurant_information_finder(place_id):
    place_id_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
    place_id_payload = {
        "place_id": place_id,
        "key": Config.GOOGLE_API_KEY
    }
    place_id_response = requests.get(place_id_endpoint, params=place_id_payload,
                                     headers={'User-Agent': 'Google Chrome'})
    place_id_response_json = json.loads(place_id_response.text)
    print(place_id_response.text)
    results = {}
    results["name"] = place_id_response_json["result"]["name"]
    results["address"] = place_id_response_json["result"]["formatted_address"]
    try:
        results["phone"] = place_id_response_json["result"]["formatted_phone_number"]
    except KeyError:
        results["phone"] = "N/A"
    try:
        results["price"] = place_id_response_json["result"]["price_level"]
    except KeyError:
        results["price"] = "N/A"
    finally:
        results["website"] = place_id_response_json["result"]["website"]
        results["latitude"] = place_id_response_json["result"]["geometry"]["location"]["lat"]
        results["longitude"] = place_id_response_json["result"]["geometry"]["location"]["lng"]
    return results


def get_user_location():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    path = f"https://ipinfo.io/{client_ip}?token={Config.ipinfo_token}"
    response = requests.get(path, headers={'User-Agent': 'Google Chrome'})
    response_dict = json.loads(response.text)
    try:
        loc = response_dict["loc"]
        latitude = loc.split(",")[0]
        longitude = loc.split(",")[1]
        coordinates = {"latitude": latitude, "longitude": longitude}

        return coordinates
    except:
        print("trying backup plan")
        path = f"https://ipinfo.io/json"
        response = requests.get(path, headers={'User-Agent': 'Google Chrome'})
        response_dict = json.loads(response.text)
        loc = response_dict["loc"]
        latitude = loc.split(",")[0]
        longitude = loc.split(",")[1]
        coordinates = {"latitude": latitude, "longitude": longitude}

        return coordinates


def search_for_coordinates(query):
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query_name = query.replace(" ", "%20")
    response = requests.get(f"{endpoint}?query={query}&key={Config.GOOGLE_API_KEY}",
                            headers={'User-Agent': 'Google Chrome'})
    response_dict = json.loads(response.text)
    if response_dict["status"] == "ZERO_RESULTS":
        return False
    else:
        response_coordinates = {}
        response_coordinates["latitude"] = float(response_dict["results"][0]["geometry"]["location"]["lat"])
        response_coordinates["longitude"] = float(response_dict["results"][0]["geometry"]["location"]["lng"])
        return response_coordinates


def boundary_box(latitude, longitude, distance):
    # distance is in km
    earth_radius = 6378.1  # kilometers

    # define limits for lat and lon
    min_lat = math.radians(-90)
    max_lat = math.radians(90)
    min_lon = math.radians(-180)
    max_lon = math.radians(180)

    latitude = float(latitude)
    longitude = float(longitude)

    latitude_radians = math.radians(latitude)
    longitude_radians = math.radians(longitude)

    if earth_radius < 0 or distance < 0:
        raise Exception("Invalid Arguments")

    # Angular radius of query circle
    ang_radius = distance / earth_radius

    # Finding lower and upper bounds of latitude
    lat_lower = latitude_radians - ang_radius
    lat_upper = latitude_radians + ang_radius

    # Finding lower and upper bounds of longitude

    if lat_lower > min_lat and lat_upper < max_lat:
        delta_longitude = math.asin(math.sin(ang_radius)) / math.cos(latitude_radians)

        lon_lower = longitude_radians - delta_longitude
        if lon_lower < min_lon:
            lon_lower += 2 * math.pi

        lon_upper = longitude_radians + delta_longitude
        if lon_upper > max_lon:
            lon_upper -= 2 * math.pi

    else:
        lat_lower = max(lat_lower, min_lat)
        lat_upper = min(lat_upper, max_lat)
        lon_lower = min_lon
        lon_upper = max_lon

    lat_lower = math.degrees(lat_lower)
    lat_upper = math.degrees(lat_upper)
    lon_lower = math.degrees(lon_lower)
    lon_upper = math.degrees(lon_upper)

    boundary_box = {
        "lower_latitude": lat_lower,
        "upper_latitude": lat_upper,
        "lower_longitude": lon_lower,
        "upper_longitude": lon_upper
    }

    return boundary_box
