import scrapy
import random

class AmazonBooksSpider(scrapy.Spider):
    name = "amazon_books"
    allowed_domains = ["amazon.in"]
    start_urls = [
        'https://www.amazon.in/s?k=Stephen+Hawking+Books'
    ]

    # Define the list of user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # 3 seconds delay between requests
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers={'User-Agent': random.choice(self.user_agents)},
                callback=self.parse
            )

    def parse(self, response):
        books = response.xpath('//*[contains(concat(" ", @class, " "), concat(" ", "puisg-row", " "))]')
        for book in books:
            yield {
                'name': book.xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]/text()').get(),
                'price': book.xpath('.//*[contains(concat(" ", @class, " "), concat(" ", "a-price-whole", " "))]/text()').get(),
                'rating': book.xpath('.//*[contains(concat(" ", @class, " "), concat(" ", "aok-align-bottom", " "))]/span/text()').get()
            }

        next_page = response.xpath('//li[@class="a-last"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse, headers={'User-Agent': random.choice(self.user_agents)})

