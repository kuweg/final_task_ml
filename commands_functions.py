from data_fetching.cities_config import CityConfigs
from data_fetching.data_parser import DataFetcher
from data_processing.data_filter import DataFilter
from data_processing.visualization import Visualization
import os


def get_cities_list(args):
    if args.config:
        print(CityConfigs.get_cities_list())


def plot_bins_func(args):
    vis = Visualization('data/cian_data_processed.json')
    if args.bins:
        vis.draw_bar_plots()


def fetch_data_func(args):

    if args.city_config not in CityConfigs.get_cities_list():
        raise AttributeError("Unknow city config was passed. Use 'list' to display list of available citites.")

    fetcher = DataFetcher(args.city_config)

    if args.check:
        if os.path.exists(fetcher.get_raw_file_path()):
            print('Cached file with raw data already exists, override it?')
            choice = input('Please, confirm action. [Y/N]: ')
            if choice in ['Y', 'y']:
                fetcher.fetch_data()
            elif choice in ['N', 'n']:
                pass
        else:
            fetcher.fetch_data()

    filter_ = DataFilter(fetcher.get_raw_file_path())
    filter_.save_filtered_data()
