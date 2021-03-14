import pandas as pd
import requests
from bs4 import BeautifulSoup

from .utils import generate_headers


class BookingCities:
    """
    Scrapes Lithuania cities and their ids on Booking.com website.
    Id is necessary for the link in further scraping.
    """
    def __init__(self) -> None:
        self.__url = f"https://www.booking.com/searchresults.en-gb.html" \
                     f"?dest_id=122;dest_type=country"

    def get(self) -> pd.DataFrame:
        """Returns dataframe of cities with columns name and city_id."""
        result = []

        source = requests.get(self.__url, headers=generate_headers())
        soup = BeautifulSoup(source.content, "lxml")

        cities = soup.select("div#filter_uf a.filterelement")

        for city in cities:
            city_data = {}

            city_data["city_id"] = city.get("data-value")
            city_data["name"] = city.select_one(
                "span.filter_label").text.strip()

            result.append(city_data)

        return pd.DataFrame(result)
