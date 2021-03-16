import pytest
from datetime import datetime, timedelta

from lt_booking_scraper.utils import extract_number, validate_date, generate_headers


def test_generate_headers_accept():
    header = generate_headers()
    assert 'Accept' in header


def test_generate_headers_user_agent():
    header = generate_headers()
    assert 'User-Agent' in header


@pytest.mark.parametrize("value, expected", [
    ("1.5 km from centre", 1.5),
    ("from centre 1.5 km", 1.5),
    ("from 1.5 km centre", 1.5),
    ("1.5km from centre", 1.5),
])
def test_extract_number(value, expected):
    assert extract_number(value) == expected


def test_validate_date():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    assert validate_date(date) == now.date()


def test_validate_date_in_the_past():
    yesterday = datetime.now() - timedelta(days=1)
    date = yesterday.strftime("%Y-%m-%d")
    with pytest.raises(ValueError):
        validate_date(date)
