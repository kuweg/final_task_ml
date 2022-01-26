from ctypes import ArgumentError
import os

from data_fetching.cities_config import CityConfigs
from data_fetching.data_parser import DataFetcher
from data_processing.data_filter import DataFilter
from data_processing.visualization import Visualization


def get_cities_list(args):
    if args.config:
        print(CityConfigs.get_cities_list())


def plot_bins_func(args):
    vis = Visualization("data/cian_data_processed.json")
    if args.bins:
        vis.draw_bar_plots()


def save_heatmap(args):
    vis = Visualization("data/cian_data_processed.json")
    if args.heat:
        vis.draw_heatmap()
    if args.scatter:
        vis.draw_scatter_map()


def filter_data_func(args):
    if not os.path.exists(args.file):
        raise FileExistsError(
            "Cannot locate file."
        )
    if args.city not in CityConfigs.get_cities_list():
        raise AttributeError(
            "Unknow city config was passed."
            "Use 'list' to display list of available citites."
        )
    filter_ = DataFilter(args.file, args.city)
    print(filter_.get_filtered_file_path())
    if os.path.exists(filter_.get_filtered_file_path()):
        print('File already exists, override it?')
        choice = input("Please, confirm action. [Y/N]: ")
        if choice in ['Y', 'y']:
            filter_.save_filtered_data()
        elif choice in ['N', 'n']:
            pass
        else:
            raise ArgumentError(
                    "Only 'Y/N' can be accepted."
                )


def fetch_data_func(args):

    if args.city_config not in CityConfigs.get_cities_list():
        raise AttributeError(
            "Unknow city config was passed."
            "Use 'list' to display list of available citites."
        )

    fetcher = DataFetcher(args.city_config)

    if args.check:
        if os.path.exists(fetcher.get_raw_file_path()):
            print("Cached file with raw data already exists, override it?")
            choice = input("Please, confirm action. [Y/N]: ")
            if choice in ["Y", "y"]:
                fetcher.fetch_data()
            elif choice in ["N", "n"]:
                pass
            else:
                raise ArgumentError(
                    "Only 'Y/N' can be accepted."
                )
        else:
            fetcher.fetch_data()

    filter_ = DataFilter(fetcher.get_raw_file_path(),
                         args.city_config)
    filter_.save_filtered_data()
