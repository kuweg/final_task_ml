import argparse

from command_functions import (fetch_data_func,
                               filter_data_func,
                               get_cities_list,
                               plot_bins_func,
                               save_heatmap,)

parser = argparse.ArgumentParser(
            description=("An app for parsing a 'https://cian.ru"
                         "and visualize statistics from it.")
            )

subparser = parser.add_subparsers(
            title='subcommands',
            description='valid commands',
            help='description')

cities_config_parser = subparser.add_parser(
            'list',
            help='display a list of available citites to parse')

cities_config_parser.add_argument(
            '-show',
            action='store_true',
            default=True,
            dest='config',
            help='display a list of available citites to parse')

cities_config_parser.set_defaults(func=get_cities_list)

fetch_data = subparser.add_parser(
            'fetch_data',
            help="running a script to parse data from 'https://cian.ru'")
fetch_data.add_argument(
            'city_config',
            type=str,
            help='City config file name')

fetch_data.add_argument(
            '-info',
            action='store_true',
            default=True, dest='check',
            help='checks if cached raw data exists.')
fetch_data.set_defaults(func=fetch_data_func)

plot_bins = subparser.add_parser(
            'plot_bins',
            help="creates bin plots at save them at '..output/' folder")

plot_bins.add_argument(
            '-save',
            action='store_true',
            default=True,
            dest='bins',
            help='save the bar plots.')

plot_bins.set_defaults(func=plot_bins_func)

heatmap = subparser.add_parser(
            'heatmap',
            help=("creates a heatmap of parsed city"
                  "and saves it at '..output/' folder"))

heatmap.add_argument(
            '-save',
            action='store_true',
            default=True,
            dest='heat',
            help='Saves a hetmap at html file')

heatmap.add_argument(
            '-scatter',
            action='store_true',
            dest='scatter',
            help='Plots scatter version of heatmap.')

heatmap.set_defaults(func=save_heatmap)

filter_data = subparser.add_parser(
            'filter',
            help=('manually apply filter script to'
                  'to provided file'))
filter_data.add_argument(
            'file',
            type=str,
            help='Path to file')

filter_data.add_argument(
            'city',
            type=str,
            help='City name for correct output file')

filter_data.set_defaults(func=filter_data_func)


if __name__ == "__main__":
    parsed_args = parser.parse_args()
    parsed_args.func(parsed_args)
