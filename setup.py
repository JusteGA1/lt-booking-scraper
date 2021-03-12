from distutils.core import setup

setup(
    name='lt_booking_scraper',
    version='1.0',
    packages=['lt_booking_scraper'],
    url='https://github.com/JusteGA1/lt-booking-scraper',
    license='MIT License',
    author='Juste Gaviene',
    author_email='juste.gaviene@gmail.com',
    description='Booking.com scraper for Lithuania hotels. Scrapes cities, '
                'hotels info and prices.',
    install_requires=[
        'requests',
        'bs4',
        'pandas',
        'fake_headers',
        'nums_from_string'
    ]
)
