import re
import scrapy
from books_to_scrape.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        genre_names = response.css("div.side_categories ul.nav.nav-list li a::text").getall()
        genre_links = response.css("div.side_categories ul.nav.nav-list li a::attr(href)").getall()
        

        for name, link in zip(genre_names[1:], genre_links[1:]):
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_book_information,
                meta={
                    'genre_name': name.strip(),
                    'genre_link': response.urljoin(link)
                }
            )

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_book_information(self, response):
        book_links = response.css('article.product_pod h3 a::attr(href)').getall()

        genre_name = response.meta.get('genre_name')
        genre_link = response.meta.get('genre_link')

        for link in book_links:
            book_link = response.urljoin(link)
            yield scrapy.Request(
                url=book_link,
                callback=self.parse_individual_book,
                meta={
                    'genre_name': genre_name,
                    'genre_link': genre_link
                }
            )

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse_book_information)

    def parse_individual_book(self, response):
        title = response.css('div.product_main h1::text').get() 
        image_url = response.css('div#product_gallery div.carousel-inner div.item img::attr(src)').get()
        description = response.css('#product_description + p::text').get(default='').strip()
        table_info = response.css('table.table.table-striped tr td::text').getall()
        genre = response.css('ul.breadcrumb li:nth-child(3) a::text').get()

        book_item = BookItem()
        book_item['link'] = response.url
        book_item['genre'] = genre
        book_item['title'] = title
        book_item['image_url'] = response.urljoin(image_url)
        book_item['description'] = description.rstrip(' ...more')
        book_item['upc'] = table_info[0]
        book_item['product_type'] = table_info[1]
        book_item['price_excluding_tax'] = table_info[2].replace('£', '') 
        book_item['price_including_tax'] = table_info[3].replace('£', '')
        book_item['tax'] = table_info[4].replace('£', '')
        book_item['availability'] = re.search(r'\((\d+)', table_info[5]).group(1) 
        book_item['number_of_reviews'] = table_info[6]

        yield book_item
