import json
from pprint import pprint

def fetch_data(data):
        offers = []
        for page in data:
            for item in page['data']['jsonQuery']:
                # print(type(item))
                offers.append(item['_type'])
        return offers


if __name__ == '__main__':
    with open('cian_raw_data.json') as file:
        data = json.load(file)

    a = fetch_data(data)
    pprint(a)
    