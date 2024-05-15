import scrapy


class Country:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'name': self.name, 'url': self.url}


class Offer:
    def __init__(self, name, url, description, country):
        self.name = name
        self.url = url
        self.description = description
        self.country = country

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'name': self.name, 'url': self.url, 'description': self.description, 'country': self.country}


class TrendtoursSpider(scrapy.Spider):
    name = "trendtours"
    allowed_domains = ["trendtours.de"]
    start_urls = ['https://www.trendtours.de/reiseziele']

    def parse(self, response, **kwargs):
        countries_found = []

        for country_lists in response.css('div.countries'):
            if country_lists.css('h2::text').get() != "Top-Reiseziele":
                self.parse_country_list(country_lists, countries_found, response)

        for country in countries_found:
            yield scrapy.Request(url=country.url, callback=self.parse_country, meta={'country': country})

    @staticmethod
    def parse_country_list(div, found_countries, response):
        for country in div.css('div.card.teaser.countryTeaser.border-0'):
            country_name = country.css('a div.countryTeaser-img-overlay.teaser-img-overlay::text').get()
            country_link = country.css('a::attr(href)').get()
            if not (country_name and country_link):
                raise Exception("Each country should have a name and href. The website code might have changed")
            else:
                country_data = Country(country_name, response.urljoin(country_link))
                found_countries.append(country_data)

    @staticmethod
    def parse_country(response):
        country = response.meta['country']
        offers_found = []

        for offer in response.css('a.product-teaser__outer'):
            offer_name = offer.xpath('div/div[2]/div/div[1]/div[1]/p/text()').get()
            offer_short_description = offer.xpath('div/div[2]/div/div[1]/div[2]/p/text()').get()
            offer_link = offer.css('a::attr(href)').get()

            if offer_name and offer_link:
                found_offer = Offer(offer_name, offer_link, offer_short_description, str(country))
                offers_found.append(found_offer)

        for offer in offers_found:
            yield offer.to_dict()
