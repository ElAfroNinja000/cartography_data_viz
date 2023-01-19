import os
import pandas as pd
import folium
import webbrowser

DATA_PATH = f"{os.getcwd()}/data/"


def build_df_by_countries():
    df_raw = pd.read_csv(f"{DATA_PATH}world_countries.csv")
    df_countries_data = df_raw[["country", "population", "pop_density", "net_migration", "infant_mortality", "gdp",
                                "literacy", "phones", "climate", "birth_rate", "death_rate", "agriculture", "industry",
                                "service"]].fillna(0)
    df_countries_coords = pd.read_csv(f"{DATA_PATH}countries_coords.csv")

    return pd.merge(left=df_countries_data, right=df_countries_coords, left_on="country", right_on="country")


def country_data_to_popup(country_name, infant_mortality, gdp):
    return f""" {country_name}
    Infant Mortality: {infant_mortality}
    GDP: {gdp}
    """


if __name__ == "__main__":
    df = pd.read_csv(f"{DATA_PATH}data_by_countries.csv")

    center_point = df[["latitude", "longitude"]].mean().values.tolist()
    south_west = df[["latitude", "longitude"]].min().values.tolist()
    north_east = df[["latitude", "longitude"]].max().values.tolist()

    map = folium.Map(location=center_point, tiles="Stamen Toner")
    for lat, lng, country, infant_mortality, gdp in zip(df["latitude"], df["longitude"], df["country"], df["infant_mortality"], df["gdp"]):
        folium.Marker([lat, lng], popup=f"{country_data_to_popup(country, infant_mortality, gdp)}", tooltip=f"{lat}, {lng}").add_to(map)
    map.fit_bounds([south_west, north_east])
    map.save(f"{DATA_PATH}map.html")
    webbrowser.open(f"{DATA_PATH}map.html")