import json
import os
import random
import time
from typing import Generator

from fake_useragent import UserAgent
import requests

from .cities_config import CityConfigs
from .variables import CACHE_FILE, CIAN_API_URL, DATADIR, REFERER


class DataFetcher:
    def __init__(self, city_config_name: str, file_path: str = None) -> None:
        self.city_config = CityConfigs.get_city_params(city_config_name)
        self._cache_file_path = (
            file_path if file_path is not None
            else (DATADIR + CACHE_FILE.format(city_config_name))
        )

    def get_raw_file_path(self) -> str:
        return self._cache_file_path

    @staticmethod
    def check_file_existance(path_to_file: str) -> None:
        if not os.path.exists(path_to_file):
            open(path_to_file, "w").close()

    def config_payload(self, page: int) -> dict:
        post_request = {
            "jsonQuery": {
                "region": {
                           "type": "terms",
                           "value": [self.city_config["cityId"]]
                        },
                "_type": "flatsale",
                "room": {
                    "type": "terms",
                    "value": [1, 2, 3, 4, 5, 6]
                    },
                "engine_version": {
                    "type": "term",
                    "value": 2
                    },
                "page": {
                    "type": "term",
                    "value": page
                    },
            }
        }
        return post_request

    def fetch_pages(self) -> Generator:
        """
        Combine pages from city config into generator.
        """
        return range(
            self.city_config["first_page"],
            self.city_config["last_page"] + 1
            )

    def fetch_data(self) -> None:
        fake_user_agent = UserAgent()
        pages = self.fetch_pages()
        DataFetcher.check_file_existance(self._cache_file_path)
        dumping_data = []

        for page_number in pages:
            user_agent = {"user-agent": fake_user_agent.random}
            headers = user_agent | REFERER
            json_request = self.config_payload(page_number)
            try:
                response = requests.post(CIAN_API_URL,
                                         headers=headers,
                                         json=json_request)
            except (ConnectionError, ConnectionResetError) as exc:
                print('Connection problems')
                print(exc)
                continue
            if response.status_code == 200:
                try:
                    receivied_data = response.json()
                    print(f"Parsed {page_number}!")
                    dumping_data.append(receivied_data)
                    time.sleep(random.randint(3, 7))
                except Exception as exc:
                    print(f"Page {page_number} wasn't fetched with")
                    print(exc)
                    time.sleep(random.randint(3, 7))
            else:
                print("Something went wrong. Cannot recieve post request")
        print('Dumping collected data to json...')
        with open(self._cache_file_path, "w") as json_file:
            json.dump(dumping_data, json_file, indent=4)
