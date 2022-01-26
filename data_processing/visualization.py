import branca.colormap as cm
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .variables import OUTPUT_DIR, PARAMS


class Visualization:
    def __init__(self, filename) -> None:
        self.df = pd.read_json(filename)
        self._set_price_per_meter()

    def _set_price_per_meter(self) -> None:
        self.df["per_meter"] = self.df["price"] / self.df["space"]

    @staticmethod
    def _plot_disctrict_bar_statistic(
        district_names: list,
        values: list,
        bar_title: str,
        x_label: str,
        y_label: str,
        params: dict,
        save_name: str,
    ) -> None:

        plt.rcParams.update(params)
        fig, ax = plt.subplots()
        sns.set_style("darkgrid")
        bar = sns.barplot(x=values, y=district_names)
        bar.set(xlabel=x_label, ylabel=y_label, title=bar_title)
        ax.bar_label(bar.containers[0], fmt="%.2f")
        plt.savefig(save_name, bbox_inches="tight")
        bar.containers = []

    def get_boundaries(self) -> tuple:
        right = self.df["lng"].max()
        left = self.df["lng"].min()
        top = self.df["lat"].max()
        bottom = self.df["lat"].min()
        return (right, left, top, bottom)

    def get_map_center(self) -> tuple:
        city_coords = self.get_boundaries()
        coordX = (city_coords[0] + city_coords[1]) / 2
        coordY = (city_coords[2] + city_coords[3]) / 2
        return (coordY, coordX)

    def draw_bar_plots(self):
        districts_group = self.df.groupby("district_name")
        district_names = districts_group.mean()["price"].keys()
        prices = districts_group.mean()["price"].values / 10**6
        prices_per_meter = (
            districts_group.mean()["per_meter"].values
        )
        spaces = districts_group.mean()["space"].values

        Visualization._plot_disctrict_bar_statistic(
            district_names=district_names,
            values=prices,
            bar_title="Comparison of mean flat prices by districts",
            x_label="Price, MM",
            y_label="District",
            params=PARAMS,
            save_name=OUTPUT_DIR + "price.png",
        )

        Visualization._plot_disctrict_bar_statistic(
            district_names=district_names,
            values=spaces,
            bar_title="Comparison of mean flat spaces by districts",
            x_label="Meters, m^2",
            y_label="District",
            params=PARAMS,
            save_name=OUTPUT_DIR + "space.png",
        )

        Visualization._plot_disctrict_bar_statistic(
            district_names=district_names,
            values=prices_per_meter,
            bar_title="Comparison of mean meter prices by districts",
            x_label="Price",
            y_label="District",
            params=PARAMS,
            save_name=OUTPUT_DIR + "meter_prices.png",
        )

    def draw_heatmap(self):
        start_point = self.get_map_center()
        map = folium.Map(location=[start_point[0],
                                   start_point[1]],
                         zoom_start=9)
        lat = self.df['lat'].to_list()
        long = self.df['lng'].to_list()
        price = self.df['per_meter'].to_list()

        HeatMap(list(zip(lat, long, price)), radius=10, blur=10).add_to(map)
        map.save(OUTPUT_DIR + 'heatmap.html')

    def draw_scatter_map(self):
        start_point = self.get_map_center()
        min_price = self.df.groupby("district_name").mean()["per_meter"].min()
        max_price = self.df.groupby("district_name").mean()["per_meter"].max()
        colormap = cm.LinearColormap(
            colors=["green", "yellow", "red"], vmin=min_price, vmax=max_price
        )
        map = folium.Map(location=(start_point[0],
                                   start_point[1]),
                         zoom_start=10)
        for i in range(len(self.df)):
            folium.Circle(
                location=[self.df.iloc[i]["lat"], self.df.iloc[i]["lng"]],
                radius=1000,
                fill=True,
                color=colormap(self.df.iloc[i]["per_meter"]),
                fill_opacity=0.2,
                opacity=0.1,
            ).add_to(map)
        map.add_child(colormap)
        map.save(OUTPUT_DIR + "scatter_map.html")
