
class CityConfigs:

    _cities = {
            'spb': {
            'cityId': 2,
            'first_page': 1,
            'last_page': 41
            },
            'msc': {
            'cityId': 1,
            'first_page': 1,
            'last_page': 41
            }
        }

    @staticmethod
    def get_city_params(key):
        return CityConfigs._cities[key]

    @staticmethod
    def count_cities():
        return len(CityConfigs._cities.keys())

    @staticmethod
    def get_cities_list():
        return list(CityConfigs._cities.keys())
    
