import os
import folium
import webbrowser
import pandas as pd
from make_popup import PopupMaker as pm

DATA_PATH = f"{os.getcwd()}/data/"
HTML_PATH = f"{os.getcwd()}/html/"
TILES = ["cartodbpositron", "OpenStreetMap", "Stamen Terrain", "Stamen Toner", "cartodbdark_matter"]
METRICS_INCREASING = ["population", "net_migration", "gdp", "literacy", "phones", "birth_rate"]
METRICS_DECREASING = ["pop_density", "infant_mortality", "death_rate"]
COLORS    = ["darkred", "red", "lightred", "orange", "lightgreen", "green", "darkgreen"]


# This class takes a CSV file and a ranking metric as input, and builds a map with markers that are colored based on the ranking
# metric
class WorldDataAnalytics:
    def __init__(self, input_file: str, ranking_metric: str):
        self.df = pd.read_csv(f"{DATA_PATH}{input_file}", thousands=',')
        center_point = self.df[["latitude", "longitude"]].mean().values.tolist()
        south_west   = self.df[["latitude", "longitude"]].min().values.tolist()
        north_east   = self.df[["latitude", "longitude"]].max().values.tolist()
        self.map_obj = folium.Map(location=center_point, tiles=TILES[0])
        for tile in TILES:
            folium.TileLayer(tile).add_to(self.map_obj)
        self.map_obj.fit_bounds([south_west, north_east])
        self.ranking_metric = ranking_metric

    def __display_map__(self):
        """
        > This function takes the map object and adds a layer control to it, then saves the map object as an html file and
        opens it in a web browser
        """
        folium.LayerControl().add_to(self.map_obj)
        self.map_obj.save(f"{HTML_PATH}{self.ranking_metric}.html")
        webbrowser.open(f"{HTML_PATH}{self.ranking_metric}.html")

    """
    > This function takes a country name and a dictionary of metrics for that country, and returns a folium popup object
    that contains a table of the metrics

    :param country_name: str
    :type country_name: str
    :param country_metrics: a dictionary of metrics for a given country
    :type country_metrics: dict
    :return: A folium.Popup object.
    """
    def __country_data_to_popup__(self, country_name: str, country_metrics: dict):
        popup_text = pm(country_name, country_metrics).make_html_popup()
        return folium.Popup(popup_text)

    """
    This function takes a country name, latitude, longitude, ranking metric, and popup, and returns a marker with a color
    corresponding to the country's ranking in the given metric

    :param country_name: The name of the country to be plotted
    :type country_name: str
    :param lat: latitude of the marker
    :type lat: float
    :param lng: longitude
    :type lng: float
    :param ranking_metric: the metric to use for ranking countries
    :type ranking_metric: str
    :param popup: the popup that will appear when you click on the marker
    :type popup: folium.Popup
    :return: A folium.Marker object
    """
    def __make_ranked_marker__(self, country_name: str, lat: float, lng: float, ranking_metric: str, popup: folium.Popup):
        ranking = self.df.loc[self.df['country'] == country_name].iloc[0]["ranking"]
        ranking = abs(len(COLORS) - ranking - 1) if ranking_metric in METRICS_DECREASING else ranking
        color = COLORS[ranking]
        icon = folium.Icon(color=color)
        marker = folium.Marker([lat, lng], popup=popup, tooltip=country_name, icon=icon)
        return marker

    """
    > For each country in the dataframe, create a feature group, create a popup, create a marker, and add the marker to
    the feature group
    """
    def build_map_from_data(self):
        self.df = self.df.reset_index()
        self.df["ranking"] = pd.qcut(pd.to_numeric(self.df[self.ranking_metric].rank(method='first')), len(COLORS), labels=False)
        for index, row in self.df.iterrows():
            feature_group = folium.FeatureGroup(row["country"])
            country_metrics = dict(zip(metrics, [row[metric] for metric in metrics]))
            popup = self.__country_data_to_popup__(row["country"], country_metrics)
            self.__make_ranked_marker__(row["country"], row["latitude"], row["longitude"],
                                        self.ranking_metric, popup).add_to(feature_group)
            feature_group.add_to(self.map_obj)
        self.__display_map__()


if __name__ == "__main__":
    metrics = METRICS_INCREASING + METRICS_DECREASING
    wda = WorldDataAnalytics("data_by_countries.csv", "population")
    wda.build_map_from_data()
