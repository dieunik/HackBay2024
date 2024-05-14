import scrapy


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
                self.parse_country_list(country_lists, top_countries_found, response)
            else:
                self.parse_country_list(country_lists, countries_found, response)

        for country in top_countries_found + countries_found:
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
        offers = []
        for offer in response.css('a.product-teaser__outer'):
            offer_name = offer.xpath('div/div[2]/div/div[1]/div[1]/p/text()').get()
            offer_link = offer.css('a::attr(href)').get()
            offers.append(Offer(offer_name, response.urljoin(offer_link)))

        country.offers = offers
        yield {
            'country': str(country),
            'offers': [{'name': offer.name, 'url': offer.url} for offer in offers]
        }