import logging

import httpx
import requests

import constants


async def get_weather(update, context, coordinates):
    async with httpx.AsyncClient() as client:
        weather_response = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={coordinates['lat']}&longitude={coordinates['lng']}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        )
        weather = weather_response.json()
    return weather["current_weather"]


def extract_lat_long_via_address(address_or_zipcode):
    lat, lng = None, None
    api_key = constants.GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        """
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        """
        results = r.json()["results"][0]
        lat = results["geometry"]["location"]["lat"]
        lng = results["geometry"]["location"]["lng"]

        city_name = None
        country_name = None

        address_components = results.get("address_components", [])
        for component in address_components:
            types = component.get("types", [])
            if "locality" in types:
                city_name = component.get("long_name")
            elif "country" in types:
                country_name = component.get("long_name")

        location = f"{city_name}, {country_name}"
    except:
        location = None
    return lat, lng, location
