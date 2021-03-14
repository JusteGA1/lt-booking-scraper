# Booking.com scraper of hotels in Lithuania

Module is intended for scraping hotels on Booking.com in Lithuania. It has 3 classes which scrapes:
- cities for city id for further scraping;
- hotels data for requested city;
- hotels prices for specific check-in date.   
NOTE: scraper is written only for hotels data, not all accommodation properties. 

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Code Examples](#code-examples)
* [Status](#status)
* [License](#license)
* [Disclaimer](#disclaimer)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
Scraper was written for learning purposes.  
Project contains two Python files: one for site scrapping, another with supporting functions. 

Scrape cities first in order to get city id for usage of other classes. Check [code examples](#code-examples) for expected input of city. 

For BookingHotels class you can indicate the minimum amount of stars hotel should have, default is 3 stars. Scraped data: hotel_id, title, number of stars, longitude and latitude, distance from the city centre, review score and amount. Booking.com recommends to update this information once per week.

BookingHotelsPrices scrapes only hotel id and price for specific night. Number of nights can be changed, but note that it scrapes total price, not price per night. Booking.com recommends to update this information at least once per hour. 

BookingHotels and BookingHotelsPrices dataframes can be easily merged on hotel id. Both classes return dataframes without duplicates which often happen due to specific Booking.com algorithm. 

## Technologies
* Python - version 2.8.1
* pandas - version 1.2.3
* beautifulsoup4 - version 4.9.3
* requests - version 2.25.1  
* fake-headers - version 1.0.2 
   
_for more please read requirements.txt_

## Setup
- to your notebook:
```python
!pip install git+https://github.com/JusteGA1/lt-booking-scraper

from lt_booking_scraper import BookingCities, BookingHotels, BookingHotelsPrices
```

## Code Examples
```python
booking_cities = BookingCities()
cities = booking_cities.get()

vilnius = cities[cities["name"] == "Vilnius"].iloc[0]

booking_hotels = BookingHotels()
hotels = booking_hotels.get(75, vilnius)

hotels_prices = BookingHotelsPrices()
prices = hotels_prices.get(vilnius, 75, "2021-05-08")
```

## Status
Project is: _finished_

## License
>You can check out the full license [here](https://opensource.org/licenses/MIT)

This project is licensed under the terms of the **MIT** license.

## Disclaimer

Data fetched from booking is only for personal use, you are not allowed to copy and paste content from Booking.com on to your own or third party pages (including social media pages such as Facebook, Twitter, Instagram etc.).

This applies to all types of content that can be found on Booking.com pages, including but not limited to hotel descriptions, reviews, hotel and room photos, hotel facility information, and prices. Moreover, this restriction also applies to content from Booking.com partner hotel websites and Booking Holdings Group company brands: such as Agoda, Priceline, Kayak, OpenTable, Rentalcars.

Clause 4.1.5 from Booking.com Affiliate Agreement: The Affiliate shall not programmatically evaluate and extract information (including guest reviews) from any part of the Booking.com Website (e.g. screen scrape).

## Inspiration
Learning @Turing College

## Contact
Created by [Juste Gaviene](mailto:juste.gaviene@gmail.com?subject=[GitHub]%20Source%20Han%20Sans)
