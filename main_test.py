import time
from data_fetching.data_parser import DataFetcher
from data_fetching.cities_config import CityConfigs
from data_processing.data_filter import DataFilter
from data_processing.visualization import Visualization

a = DataFetcher('spb')
data_filter = DataFilter(a._cache_file_path)
start_time = time.time()
filtered_data = data_filter.get_filtered_file_path()
visualization = Visualization(filtered_data)
visualization.draw_bar_plots()
print("--- %s seconds ---" % (time.time() - start_time))