import pandas as pd
import os

import folium
from dotenv import load_dotenv
if "DEBUG" in os.environ:
    load_dotenv()

from helpers import institution_coordinates


def create_institution_csv():

    in_person = pd.read_excel("data/HTC23 in-person roster 7.5.23.xlsx")
    remote = pd.read_excel("data/HTC23 remote registrants.xlsx")

    institutions = set(in_person["Affiliation"].unique()).union(set(remote["Institution"].unique()))

    df = pd.DataFrame(institutions, columns=["Institution"])

    df["remote"] = df["Institution"].isin(remote["Institution"].unique())
    df["in_person"] = df["Institution"].isin(in_person["Affiliation"].unique())

    df.to_csv("data/institutions.csv", index=False)


def institutions_to_coordinates():
    institutions = pd.read_csv("data/institutions.csv")["Institution"].values

    institutions = {i: {} for i in institutions}

    for i in institutions.keys():
        institutions[i] = institution_coordinates(i)

    pd.DataFrame.from_records([{"Institution": k, **v} for k,v in institutions.items()]).to_csv("data/located_institutions.csv", index=False)


def get_joined_df():
    institution_df = pd.read_csv("data/institutions.csv")
    located_institution_df = pd.read_csv("data/institutions_mapped.csv")

    return pd.merge(institution_df, located_institution_df, on="Institution", how="left")


def mapped_institutions_to_map():
    joined_df = get_joined_df()

    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles=f"https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/tiles/{{z}}/{{x}}/{{y}}?access_token={os.environ['MAPBOX_KEY']}", attr="Maps via Mapbox")

    for row in joined_df.to_dict(orient="records"):

        red_star = folium.features.CustomIcon("/Users/clock/PycharmProjects/RegistrantMap/assets/star_red.png", icon_size=(24, 32), icon_anchor=(10, 28))
        gold_star = folium.features.CustomIcon("/Users/clock/PycharmProjects/RegistrantMap/assets/star_gold.png", icon_size=(24, 32), icon_anchor=(10, 28))

        if row['in_person'] and type(row["Geo Coordinates"]) is not float:
            folium.Marker(row["Geo Coordinates"].split(", "), icon=gold_star, popup=row['Institution']).add_to(m)

    m.save("html/in_person_institutions.html")

    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles=f"https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/tiles/{{z}}/{{x}}/{{y}}?access_token={os.environ['MAPBOX_KEY']}", attr="Maps via Mapbox")

    for row in joined_df.to_dict(orient="records"):

        red_star = folium.features.CustomIcon("/Users/clock/PycharmProjects/RegistrantMap/assets/star_red.png", icon_size=(24, 32), icon_anchor=(10, 28))
        gold_star = folium.features.CustomIcon("/Users/clock/PycharmProjects/RegistrantMap/assets/star_gold.png", icon_size=(24, 32), icon_anchor=(10, 28))

        if row['remote'] and type(row["Geo Coordinates"]) is not float:
            folium.Marker(row["Geo Coordinates"].split(", "), icon=red_star, popup=row['Institution']).add_to(m)

    m.save("html/remote_institutions.html")

    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles=f"https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/tiles/{{z}}/{{x}}/{{y}}?access_token={os.environ['MAPBOX_KEY']}", attr="Maps via Mapbox")

    for row in joined_df.to_dict(orient="records"):

        red_star = folium.features.CustomIcon("/Users/clock/PycharmProjects/RegistrantMap/assets/star_red.png", icon_size=(24, 32), icon_anchor=(10, 28))
        gold_star = folium.features.CustomIcon("/Users/clock/PycharmProjects/RegistrantMap/assets/star_gold.png", icon_size=(24, 32), icon_anchor=(10, 28))

        if row['remote'] and type(row["Geo Coordinates"]) is not float:
            folium.Marker(row["Geo Coordinates"].split(", "), icon=red_star, popup=row['Institution']).add_to(m)
        if row['in_person'] and type(row["Geo Coordinates"]) is not float:
            folium.Marker(row["Geo Coordinates"].split(", "), icon=gold_star, popup=row['Institution']).add_to(m)

    m.save("html/both_institutions.html")






if __name__ == "__main__":
    mapped_institutions_to_map()