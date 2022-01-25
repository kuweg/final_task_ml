import json

from .variables import FILTERED_DATA_FNAME, DATADIR

class DataFilter:
    
    def __init__(self, raw_data_filename: str,
                 new_file_name: str=None) -> None:
        self.raw_data = raw_data_filename
        self.filtered_data = new_file_name if new_file_name is not None else FILTERED_DATA_FNAME

    def get_filtered_file_path(self):
        return DATADIR + self.filtered_data

    @staticmethod
    def fetch_data(data):
        offers = []
        for page in data:
            for item in page['data']['offersSerialized']:
                offer = {}
                offer['cityId'] = item['geo']['address'][0]['id']
                offer['city_name'] = item['geo']['address'][0]['name']
                offer['district_name'] = item['geo']['address'][1]['fullName'].split(' ')[1]
                offer['district_id'] = item['geo']['address'][1]['id']
                offer['lat'] = item['geo']['coordinates']['lat']
                offer['lng'] = item['geo']['coordinates']['lng']
                offer['price'] = item['bargainTerms']['priceRur']
                offer['space'] = float(item['totalArea'])
                offer['url'] = item['fullUrl']
                offers.append(offer)
        return offers

    def apply_filter(self):
        with open(self.raw_data) as file:
            data = json.load(file)
        try:
            filtered_data = DataFilter.fetch_data(data)
        except Exception as exc:
            print(f'Unable to filter json file')
            print(exc)
        return filtered_data

    def save_filtered_data(self):
        data = self.apply_filter()
        with open(self.filtered_data, 'w') as file:
            json.dump(data, file, indent=4)

