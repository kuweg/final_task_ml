import random
from django.http import response
import requests
import os
import json
from variables import CIAN_API_URL, USER_AGENT, REFERER
from cities_config import spb
from typing import Generator
import time


class DataFetcher:
    def __init__(self, file_name, city_config) -> None:
        self.file_name = file_name
        self.city_config = city_config

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

    def filter_fetched_data(self):
        pass

    def fetch_data(self) -> None:
        pages = self.fetch_pages()
        self.check_file_existance(self.file_name)
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
                    time.sleep(random.randint(1, 5))
                except Exception as exc:
                    print(exc)

        with open(self.file_name, "w") as json_file:
            json.dump(dumping_data, json_file, indent=4)


if __name__ == "__main__":
    a = DataFetcher("test_cian.json", spb)
    start_time = time.time()
    a.fetch_data()
    print("--- %s seconds ---" % (time.time() - start_time))
