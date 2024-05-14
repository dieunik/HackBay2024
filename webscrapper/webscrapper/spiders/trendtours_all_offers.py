import scrapy
from enum import StrEnum


class Offer:
    name: str
    url: str

    def __init__(self, name, url):
        self.name = name
        self.url = url


class Country:
    name: str
    url: str
    offers: list[Offer]

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name


class TrendtoursAllOffersSpider(scrapy.Spider):
    name = "trendtours_all_offers"
    allowed_domains = ["trendtours.de"]
    start_urls = ['https://www.trendtours.de/reiseziele']

    def parse(self, response, **kwargs):
        top_countries_found: list[Country] = []
        countries_found: list[Country] = []

        for country_lists in response.css('div.countries'):
            if country_lists.css('h2::text').get() == "Top-Reiseziele":
                self.parse_country_list(country_lists, top_countries_found)
            else:
                self.parse_country_list(country_lists, countries_found)

        yield {
            'top_countries_found': [str(country) for country in top_countries_found],
            'countries_found': [str(country) for country in countries_found]
        }

    @staticmethod
    def parse_country_list(div, found_countries):

        for country in div.css('div.card.teaser.countryTeaser.border-0'):
            country_name = country.css('a div.countryTeaser-img-overlay.teaser-img-overlay::text').get()
            country_link = country.css('a::attr(href)').get()
            if not (country_name and country_link):
                raise Exception("Each country should have a name and href. The website code might have changed")
            else:
                country_data = Country(country_name, country.urljoin(country_link))
                found_countries.append(country_data)

    def parse_country(self, country: Country):
        pass
        
