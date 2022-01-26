import json
import os
from typing import Dict, List

from .variables import DATADIR, FILTERED_DATA_FNAME


class DataFilter:
    def __init__(self, raw_data_path: str,
                 city: str,
                 filtered_data_path: str = None
                 ) -> None:

        if os.path.exists(raw_data_path):
            self.raw_data_path = raw_data_path
        else:
            raise FileExistsError(
                "Raw data file was not found!",
                "Probably, fetching data steps were skipped!",
            )
        self.filtered_data_path = (
            filtered_data_path
            if filtered_data_path is not None
            else DATADIR + FILTERED_DATA_FNAME.format(city)
        )

    def get_filtered_file_path(self):
        return self.filtered_data_path

    @staticmethod
    def fetch_data(data: List[Dict]) -> None:
        offers = []
        for page in data:
            for item in page["data"]["offersSerialized"]:
                offer = {}
                offer["cityId"] = item["geo"]["address"][0]["id"]
                offer["city_name"] = item["geo"]["address"][0]["name"]
                dist_name = item["geo"]["address"][1]["fullName"]
                offer["district_name"] = dist_name
                offer["district_id"] = item["geo"]["address"][1]["id"]
                offer["lat"] = item["geo"]["coordinates"]["lat"]
                offer["lng"] = item["geo"]["coordinates"]["lng"]
                offer["price"] = item["bargainTerms"]["priceRur"]
                offer["space"] = float(item["totalArea"])
                offer["url"] = item["fullUrl"]
                offers.append(offer)
        return offers

    def apply_filter(self) -> List[Dict]:
        with open(self.raw_data_path) as file:
            data = json.load(file)
        try:
            filtered_data = DataFilter.fetch_data(data)
        except json.JSONDecodeError as exc:
            print("Unable to filter json file")
            print(exc)
        return filtered_data

    def save_filtered_data(self) -> None:
        data = self.apply_filter()
        with open(self.filtered_data_path, "w") as file:
            json.dump(data, file, indent=4)
