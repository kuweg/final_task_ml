import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from plot_params import PARAMS

filename = 'test_cian_filtered.json'

df = pd.read_json(filename)
df['price_pre_meter'] = df['price'] / df['space']


def plot_disctrict_bar_statistic(district_names: list, district_value: list,
                                 bar_title: str, x_label: str, y_label: str,
                                 params: dict, save_name: str) -> None:
        plt.rcParams.update(params)
        sns.set_style('darkgrid')
        bar = sns.barplot(x=district_value, y=district_names)
        bar.set(xlabel=x_label, ylabel=y_label, title=bar_title)
        plt.bar_label(bar.containers[0], fmt='%.2f')      
        plt.savefig(save_name, bbox_inches='tight')

def get_boundaries(df: pd.DataFrame) -> tuple:
    right = df['lng'].max()
    left = df['lng'].min()
    top = df['lat'].max()
    bottom = df['lat'].min()
    return (right, left, top, bottom)


def get_map_center(df: pd.DataFrame) -> tuple:
    city_coords = get_boundaries(df)
    coordX = (city_coords[0] + city_coords[1]) / 2
    coordY = (city_coords[2] + city_coords[3]) / 2
    return (coordX, coordY)

if __name__ == '__main__':
    print(get_map_center(df))