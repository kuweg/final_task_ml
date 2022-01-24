import json


class DataFilter:
    
    def __init__(self, raw_data_filename: str) -> None:
        self.raw_data = raw_data_filename

    def fetch_data(self):
        offers = []
        for page in self.raw_data:
            for item in page['data']['offersSerialized']:
                offer = {}
                offer['cityId'] = item['geo']['address'][0]['id']
                offer['city_name'] = item['geo']['address'][0]['name']
                offer['disctrict_name'] = item['geo']['address'][1]['fullName'].split(' ')[1]
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
        filtered_data = self.fetch_data(data)
        return filtered_data

    def save_filter_data(self, filterder_data_filename: str):
        data = self.apply_filter()
        with open(filterder_data_filename, 'w') as file:
            json.dump(data, file, indent=4)

