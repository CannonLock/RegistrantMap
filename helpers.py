import os
import requests

session = requests.Session()
session.headers.update({"Authorization": os.environ['RADAR_API_KEY']})

def institution_coordinates(institution: str):

    response = session.get("https://api.radar.io/v1/geocode/forward", params={"query": institution})

    try:
        address = response.json()['addresses'][0]
        del address['geometry']
    except:
        return {}

    return address
