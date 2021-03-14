import math
import random
import time
import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd
from .utils import generate_headers, extract_number, validate_date


class BookingHotelsPrices:
    """
    Scrapes hotels prices on Booking.com. Prices are dynamic and constantly
    changing, so it is recommended to update them at least once per hour.
    """
    def __init__(self, nights: int = 1) -> None:
        """Takes number of nights to put on search. Default is 1."""
        self.__nights = nights
        self.__url = f"https://www.booking.com/searchresults.en-gb.html?" \
                  f"tmpl=searchresults" \
                  f"&checkin_year_month_monthday=%CHECK_IN%" \
                  f"&checkout_year_month_monthday=%CHECK_OUT%" \
                  f"&city=%CITY_ID%&nflt=ht_id%3D204%3B" \
                  f"&rows=25&offset=%OFFSET%"

    def get(self, city: pd.Series, hotels_amount: int, checkin_date: str) -> \
        pd.DataFrame:
        """
        Scrapes given number of hotels for indicated city on provided night.
        NOTE: returns full price, not price per night.
        """
        checkin = validate_date(checkin_date)
        checkout = checkin + datetime.timedelta(days=self.__nights)
        result = []
        page_number = 0  # next page +25
        number_of_pages = math.ceil(hotels_amount / 25)

        for page in range(number_of_pages):
            time.sleep(random.randint(5, 20))
            url = self.__url \
                .replace("%CITY_ID%", str(city["city_id"])) \
                .replace("%CHECK_IN%", str(checkin)) \
                .replace("%CHECK_OUT%", str(checkout)) \
                .replace("%OFFSET%", str(page_number))

            headers = generate_headers()
            source = requests.get(url, headers=headers)
            soup = BeautifulSoup(source.content, "lxml")

            hotels = soup.select("div.sr_item")

            for hotel_tag in hotels:
                hotel_price = self.extract_hotel_price(hotel_tag)
                if not hotel_price:
                    continue
                result.append(hotel_price)

            page_number += 25

        result_df = pd.DataFrame(result)
        return result_df.drop_duplicates()

    def extract_hotel_price(self, hotel) -> dict:
        """
        Extracts hotel id for possibility to join with BookingHotel class
        dataframe and hotel's price."""
        try:
            result = {}

            result["hotel_id"] = hotel.get("data-hotelid")

            price_tag = hotel.find("div", "bui-price-display__value")
            result["price"] = extract_number(price_tag.text)

            return result

        except:
            return None
