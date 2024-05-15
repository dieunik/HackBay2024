import scrapy


class Country:
    name: str
    url: str

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {'name': self.name, 'url': self.url}


class Offer:
    name: str
    url: str
    description: str
    country: str

    def __init__(self, name, url, description, country):
        self.name = name
        self.url = url
        self.description = description
        self.country = country
    
    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {'name': self.name, 'url': self.url, 'description': self.description, 'country': self.country}


class Trendtours(scrapy.Spider):
    name = "trendtours"
    allowed_domains = ["trendtours.de"]
    start_urls = ['https://www.trendtours.de/reiseziele']
    offers_found: list[Offer] = []

    def parse(self, response, **kwargs):
        top_countries_found: list[Country] = []
        countries_found: list[Country] = []

        for country_lists in response.css('div.countries'):
            if country_lists.css('h2::text').get() == "Top-Reiseziele":
                self.parse_country_list(country_lists, top_countries_found, response)
            else:
                self.parse_country_list(country_lists, countries_found, response)

        for country in countries_found:
            scrapy.Request(url=country.url, callback=self.parse_country, meta={'country': country})
            
        yield {'offers': [offer.to_dict() for offer in self.offers_found]}

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

    def parse_country(self, response):
        country = response.meta['country']
        for offer in response.css('a.product-teaser__outer'):
            offer_name = offer.xpath('div/div[2]/div/div[1]/div[1]/p/text()').get()
            offer_short_description = offer.xpath('div/div[2]/div/div[1]/div[2]/p/text()').get()
            offer_link = offer.css('a::attr(href)').get()
            
            found_offer = Offer(offer_name, offer_link, offer_short_description, str(country))
            self.offers_found.append(found_offer)

    @staticmethod
    def parse_offer(response):
        # could be implemented in the future to add more details about the travel, but I think it is sufficient to just
        # link the original website
        raise NotImplementedError
