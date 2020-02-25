import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance
import geopy
import folium

geolocator = geopy.geocoders.Nominatim(
    user_agent="specify_your_app_name_here", timeout=1)
geocode = geopy.extra.rate_limiter.RateLimiter(
    geolocator.geocode, min_delay_seconds=0.01)

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_json(acct):
    if (len(acct) > 1):
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '25'})
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)
        js = js['users']

    return js


def get_screenname_and_location(dic):
    """
    (dict)->(list)
    Return list of lists of username and his location
    """
    ans = []
    for i in dic:
        if i["location"] != "":
            ans.append([i["screen_name"], i["location"]])
    return ans


def coordinates(lst):
    """
    (lst)->(lst)
    Find cordinates of locations and return list
    of lists with name of film and its location
    """
    ans = []
    for item in lst:
        location = geolocator.geocode(item[1])
        try:
            ans.append(
                [item[0], list((location.latitude, location.longitude))])
        except:
            pass
    return ans


def map_creation(user_name):
    """
    (str) -> FeatureGroup
    Builts a layer with locations of user's friends
    """
    res = coordinates(get_screenname_and_location(get_json(user_name)))
    user_map = folium.Map(location=[0, 0], zoom_start=2)
    for i in res:
        user_map.add_child(folium.Marker(
            location=i[1], popup=i[0], icon=folium.Icon()))

    user_map.save("mysite/templates/Map.html")
