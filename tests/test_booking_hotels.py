import pytest
from lt_booking_scraper.booking_hotels import BookingHotels


def test_extract_meters():
    tag = "1.5 km from centre"
    assert BookingHotels.extract_meters(tag, tag) == 1500



