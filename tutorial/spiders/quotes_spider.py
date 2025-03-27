import scrapy 
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name='quotes'

    start_urls=["http://quotes.toscrape.com"]

    def parse(self, response):
        self.logger.info("Bonjour, ceci est ma première petite araignée !")
        quotes = response.css("div.quote")
        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css('quote_content', "span.text::text")
            loader.add_css('tags', "a.tag::text")
            quote_item = loader.load_item()
            author_page = quote.css(".author + a::attr(href)").get()
            self.logger.info('get author page url')
            yield response.follow(author_page, callback=self.parse_author, meta={'quote_item': quote_item})

        for next_page in response.css("li.next a"):
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css('author_name', ".author-title::text")
        loader.add_css('author_birthday', ".author-born-date::text")
        loader.add_css('author_bornlocation', ".author-born-location::text")
        loader.add_css('author_bio', ".author-description::text")
        yield loader.load_item()