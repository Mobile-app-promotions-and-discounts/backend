import math
import ssl

import certifi
from geopy.geocoders import Nominatim, options

ctx = ssl.create_default_context(cafile=certifi.where())
options.default_ssl_context = ctx


def get_location_by_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent='Cherry')
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        address = location.raw['address']
        city = address.get('city', '')
        if not city:
            city = 'City not found'
        return city
    return None


def euclidean_distance(lat1, lon1, lat2, lon2):
    radius = 6371.0
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    dlat_rad = dlat * (math.pi / 180)
    dlon_rad = dlon * (math.pi / 180)
    a = (dlon_rad * math.cos(lat1 * (math.pi / 180))) ** 2 + dlat_rad**2
    c = math.sqrt(a)
    return round(radius * c * 1000)
