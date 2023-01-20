import os
import folium
import webbrowser
import pandas as pd
from make_popup import PopupMaker as pm

DATA_PATH = f"{os.getcwd()}/data/"
METRICS   = ["population", "pop_density", "net_migration", "infant_mortality", "gdp",
             "literacy", "phones", "birth_rate", "death_rate"]
COLORS    = ["darkred", "red", "lightred", "orange", "lightgreen", "green", "darkgreen"]


class WorldDataAnalytics:
    def __init__(self, input_file: str, output_file: str):
        self.df = pd.read_csv(f"{DATA_PATH}{input_file}", thousands=',')
        center_point = self.df[["latitude", "longitude"]].mean().values.tolist()
        south_west   = self.df[["latitude", "longitude"]].min().values.tolist()
        north_east   = self.df[["latitude", "longitude"]].max().values.tolist()
        self.map_obj = folium.Map(location=center_point, tiles="cartodbpositron")
        self.map_obj.fit_bounds([south_west, north_east])
        self.output_file = output_file

    def __display_map__(self, output_name: str):
        folium.LayerControl().add_to(self.map_obj)
        self.map_obj.save(f"{DATA_PATH}{output_name}")
        webbrowser.open(f"{DATA_PATH}{output_name}")

    def __country_data_to_popup__(self, country_name: str, country_metrics: dict):
        popup_text = pm(country_name, country_metrics).make_html_popup()
        return folium.Popup(popup_text)

    def __make_ranked_marker__(self, country_name: str, lat: float, lng: float, popup: folium.Popup):
        color = COLORS[self.df.loc[self.df['country'] == country_name].iloc[0]["ranking"]]
        icon = folium.Icon(color=color)
        marker = folium.Marker([lat, lng], popup=popup, tooltip=country_name, icon=icon)
        return marker

    def build_map_from_data(self, metrics: list, ranking_metric: str):
        self.df = self.df.reset_index()
        self.df["ranking"] = pd.qcut(pd.to_numeric(self.df[ranking_metric].rank(method='first')), len(COLORS), labels=False)
        for index, row in self.df.iterrows():
            feature_group = folium.FeatureGroup(row["country"])
            country_metrics = dict(zip(metrics, [row[metric] for metric in metrics]))
            popup = self.__country_data_to_popup__(row["country"], country_metrics)
            self.__make_ranked_marker__(row["country"], row["latitude"], row["longitude"],
                                        popup).add_to(feature_group)

            feature_group.add_to(self.map_obj)
        self.__display_map__(f"{self.output_file}.html")


if __name__ == "__main__":
    for metric in METRICS:
        wda = WorldDataAnalytics("data_by_countries.csv", metric)
        wda.build_map_from_data(METRICS, metric)
