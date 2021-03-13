import math
import random
import time
import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd
from .utils import generate_headers, extract_number, validate_date


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


class BookingHotels:
    """
    Scrapes hotels static information on Booking.com.
    Though information changes rarely, it is recommended to update it once per
    week.
    """
    def __init__(self, min_stars: int = 3) -> None:
        """Takes minimum stars of hotels to scrape. Default is 3."""
        self.__url = f"https://www.booking.com/searchresults.en-gb.html?" \
              f"&tmpl=searchresults&city=%CITY_ID%&nflt=ht_id%3D204%3B" \
              f"&rows=25&offset=%OFFSET%"
        self.__stars = min_stars

    def get(self, hotels_amount: int, city: pd.Series) -> pd.DataFrame:
        """
        Scrapes given number of hotels for indicated city.
        City should be provided from BookingCities class, e.g.
        vilnius = cities[cities["name"] == "Vilnius"].iloc[0]
        """
        result = []
        page_number = 0  # next page +25
        number_of_pages = math.ceil(hotels_amount / 25)

        for page in range(number_of_pages):
            time.sleep(random.randint(5, 20))
            url = self.__url \
                .replace("%CITY_ID%", str(city["city_id"])) \
                .replace("%OFFSET%", str(page_number))

            source = requests.get(url, headers=generate_headers())
            soup = BeautifulSoup(source.content, "lxml")

            hotels = soup.select("div.sr_item")
            if len(hotels) == 0:
                print("No more hotels")
                break

            for hotel_tag in hotels:
                hotel_data = self.extract_hotel_data(hotel_tag)
                if not hotel_data:
                    continue
                result.append(hotel_data)

            page_number += 25

        result_df = pd.DataFrame(result)
        return result_df.drop_duplicates()

    def extract_hotel_data(self, hotel) -> dict:
        """
        Extracts specific hotel information: hotel_id, title, number of stars,
        longitude and latitude, distance from the city centre, review score and
        amounts.
        """
        try:
            result = {}

            result["hotel_id"] = hotel.get("data-hotelid")
            result["stars"] = int(hotel.get("data-class"))
            if result["stars"] < self.__stars:
                return None

            title_tag = hotel.find("span", class_="sr-hotel__name")
            result["title"] = title_tag.text.strip()

            location_tag = hotel.find("a", "bui-link")
            result["longitude"], result["latitude"] = location_tag \
                .get("data-coords").split(",")

            distance_tag = hotel.select_one(
                "div.sr_card_address_line span:nth-of-type(2)")
            result["distance"] = self.extract_meters(distance_tag.text)

            review_score_tag = hotel.find("div", "bui-review-score__badge")
            result["review_score"] = float(review_score_tag.text.strip())

            review_amount_tag = hotel.find("div", "bui-review-score__text")
            result["review_amount"] = extract_number(review_amount_tag.text)

            return result
        except:
            return None

    def extract_meters(self, tag: str) -> int:
        """Update distance to meters."""
        distance = extract_number(tag)
        if distance < 25:
            distance = distance * 1000
        return distance


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


