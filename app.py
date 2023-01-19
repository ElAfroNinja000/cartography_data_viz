import os
import folium
import webbrowser
import pandas as pd

DATA_PATH = f"{os.getcwd()}/data/"


class WorldDataAnalytics:
    def __init__(self, filename: str):
        self.df = pd.read_csv(f"{DATA_PATH}{filename}")
        center_point = self.df[["latitude", "longitude"]].mean().values.tolist()
        south_west =   self.df[["latitude", "longitude"]].min().values.tolist()
        north_east =   self.df[["latitude", "longitude"]].max().values.tolist()
        tiles = ["cartodbpositron", "Stamen Terrain", "Stamen Toner"]
        self.map_obj = folium.Map(location=center_point, tiles=tiles[0])
        for tile in tiles:
            folium.TileLayer(tile).add_to(self.map_obj)
        self.map_obj.fit_bounds([south_west, north_east])

    def __display_map__(self, output_name: str):
        folium.LayerControl().add_to(self.map_obj)
        self.map_obj.save(f"{DATA_PATH}{output_name}")
        webbrowser.open(f"{DATA_PATH}{output_name}")

    def __country_data_to_popup__(self, country_name: str, country_metrics: dict):
        popup_text = f"<b>{country_name}:</b>"
        for key, value in country_metrics.items():
            popup_text += f"<br>{key}: {str(value)}"
        return folium.Popup(folium.IFrame(popup_text), min_width=150, max_width=150)

    def compute_data(self, metrics):
        for lat, lng, country_name in zip(self.df["latitude"], self.df["longitude"], self.df["country"]):
            feature_group = folium.FeatureGroup(country_name)
            country_metrics = dict(zip(metrics, [self.df[metric] for metric in metrics]))
            folium.Marker([lat, lng], popup=self.__country_data_to_popup__(country_name, country_metrics),
                          tooltip=f"{lat}, {lng}").add_to(feature_group)
            feature_group.add_to(self.map_obj)
        self.__display_map__("map.html")


if __name__ == "__main__":
    metrics = ["population", "pop_density", "net_migration", "infant_mortality", "gdp",
               "literacy", "phones", "climate", "birth_rate", "death_rate"]
    wda = WorldDataAnalytics("data_by_countries.csv")
    wda.compute_data(metrics)
