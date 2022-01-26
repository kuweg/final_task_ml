class CityConfigs:
    """
    A class which stores cities config as Dict[dict] and provides
    basic manipulation such as taking city config by key,
    getting length of dict and list of cities.
    """

    # dict for cites config
    # feel free to fill it with your data
    _cities = {
        "spb": {"cityId": 2, "first_page": 1, "last_page": 41},
        "msc": {"cityId": 1, "first_page": 1, "last_page": 10},
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
