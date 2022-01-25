import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from .variables import PARAMS


class Visualization:
    
    def __init__(self, filename) -> None:
        self.df = pd.read_json(filename)

    @staticmethod
    def _plot_disctrict_bar_statistic(district_names: list, values: list,
                                      bar_title: str, x_label: str, y_label: str,
                                      params: dict, save_name: str) -> None:

        plt.rcParams.update(params)
        fig, ax = plt.subplots()
        sns.set_style('darkgrid')
        bar = sns.barplot(x=values, y=district_names)
        bar.set(xlabel=x_label, ylabel=y_label, title=bar_title)
        ax.bar_label(bar.containers[0], fmt='%.2f')      
        plt.savefig(save_name, bbox_inches='tight')
        bar.containers = []

    def get_boundaries(self) -> tuple:
        right = self.df['lng'].max()
        left = self.df['lng'].min()
        top = self.df['lat'].max()
        bottom = self.df['lat'].min()
        return (right, left, top, bottom)

    def get_map_center(self) -> tuple:
        city_coords = self.get_boundaries(self.df)
        coordX = (city_coords[0] + city_coords[1]) / 2
        coordY = (city_coords[2] + city_coords[3]) / 2
        return (coordY, coordX)

    def draw_bar_plots(self):
        self.df['price_per_meter'] = self.df['price'] / self.df['space']

        district_names = self.df.groupby('disctrict_name').mean()['price'].keys()
        prices = self.df.groupby('disctrict_name').mean()['price'].values / 10**6
        prices_per_meter = self.df.groupby('disctrict_name').mean()['price_per_meter'].values
        spaces = self.df.groupby('disctrict_name').mean()['space'].values

        Visualization._plot_disctrict_bar_statistic(
            district_names=district_names,
            values=prices,
            bar_title='Comparison of mean flat prices by districts',
            x_label='Price, MM',
            y_label='District',
            params=PARAMS,
            save_name='output/price.png'
            )

        Visualization._plot_disctrict_bar_statistic(
            district_names=district_names,
            values=spaces,
            bar_title='Comparison of mean flat spaces by districts',
            x_label='Meters, m^2',
            y_label='District',
            params=PARAMS,
            save_name='output/space.png'
            )

        Visualization._plot_disctrict_bar_statistic(
            district_names=district_names,
            values=prices_per_meter,
            bar_title='Comparison of mean meter prices by districts',
            x_label='Price',
            y_label='District',
            params=PARAMS,
            save_name='output/meter_prices.png'
            )