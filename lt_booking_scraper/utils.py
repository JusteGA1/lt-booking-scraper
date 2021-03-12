import datetime
from fake_headers import Headers
import nums_from_string


def generate_headers():
    """Generates random headers for scraping websites."""
    headers = Headers()
    result = headers.generate()
    result['Accept'] = "text/html, application/xhtml+xml, application/xml"

    return result


def extract_number(tag: str) -> int:
    """Extracts number from string."""
    return nums_from_string.get_nums(tag)[0]


def validate_date(given_date: str) -> datetime:
    """Checks if date is not in the past."""
    date = datetime.datetime.strptime(given_date, "%Y-%m-%d").date()
    if date < datetime.date.today():
        raise ValueError("Date is in the past")
    return date
