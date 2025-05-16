import scrapy


class BookItem(scrapy.Item):
    genre = scrapy.Field()
    number_of_stars = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    principal_price = scrapy.Field()
    price_excluding_tax = scrapy.Field()
    price_including_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
