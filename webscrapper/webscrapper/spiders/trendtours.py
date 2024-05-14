import scrapy


class TrendtoursSpider(scrapy.Spider):
    name = 'trendtours'
    allowed_domains = ['trendtours.de']
    start_urls = ['https://www.trendtours.de/reiseziele']

    def parse(self, response, **kwargs):
        top_countries_found = []
        countries_found = []

        for country_lists in response.css('div.countries'):
            header_text = country_lists.css('h2::text').get()
            if header_text == "Top-Reiseziele":
                self.parse_countries(country_lists, top_countries_found)
            else:
                self.parse_countries(country_lists, countries_found)

        yield {
            'top_countries_found': top_countries_found,
            'countries_found': countries_found
        }

    @staticmethod
    def parse_countries(div, found_countries):
        for country in div.css('div.card.teaser.countryTeaser.border-0'):
            title = country.css('a div.countryTeaser-img-overlay.teaser-img-overlay::text').get()
            if title:
                found_countries.append(title)
                