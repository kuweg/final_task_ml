import random
import requests
import os
import json
from .variables import CIAN_API_URL, USER_AGENT, REFERER, CACHE_FILE, DATADIR
from .cities_config import CityConfigs
from typing import Generator
import time


class DataFetcher:

    def __init__(self, city_config_name: str, file_path: str=None) -> None:
        self.city_config = CityConfigs.get_city_params(city_config_name)
        self._cache_file_path = (file_path if file_path is not None 
                                else (DATADIR+CACHE_FILE))

    def get_raw_file_path(self):
        return self._cache_file_path

    @staticmethod
    def check_file_existance(file_to_write):
        if not os.path.exists(file_to_write):
            open(file_to_write, "w").close()
            print("File was created!")
        print("Yes!")

    def config_payload(self, page: int) -> dict:
        post_request = {
            "jsonQuery": {
                "region": {"type": "terms", "value": [self.city_config["cityId"]]},
                "_type": "flatsale",
                "room": {"type": "terms", "value": [1, 2, 3, 4, 5, 6]},
                "engine_version": {"type": "term", "value": 2},
                "page": {"type": "term", "value": page},
            }
        }
        return post_request

    def fetch_pages(self) -> Generator:
        return range(self.city_config["first_page"], self.city_config["last_page"] + 1)

    def fetch_data(self) -> None:
        pages = self.fetch_pages()
        DataFetcher.check_file_existance(self._cache_file_path)
        dumping_data = []
        headers = USER_AGENT | REFERER
        for page_number in pages:
            json_request = self.config_payload(page_number)
            response = requests.post(CIAN_API_URL, headers=headers, json=json_request)
            if response.status_code == 200:
                try:
                    receivied_data = response.json()
                    print(f"Parsed {page_number}!")
                    dumping_data.append(receivied_data)
                    time.sleep(random.randint(3, 7))
                except Exception as exc:
                    print(f"Page {page_number} wasn't fetched with")
                    print(exc)
            else:
                print('Something went wrong. Cannot recieve post request')

        with open(self._cache_file_path, "w") as json_file:
            json.dump(dumping_data, json_file, indent=4)
