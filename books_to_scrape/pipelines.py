import psycopg2
from scrapy.exceptions import DropItem

class PostgreSQLPipeline:

    def open_spider(self, spider):
        # Configuração da conexão com o PostgreSQL
        self.connection = psycopg2.connect(
            host="localhost",
            database="books_to_scrape",
            user="postgres",
            password="root"
        )
        self.cursor = self.connection.cursor()

        # Criação da tabela se não existir
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                link TEXT,
                genre TEXT,
                title TEXT,
                image_url TEXT,
                description TEXT,
                upc TEXT,
                product_type TEXT,
                price_excluding_tax NUMERIC,
                price_including_tax NUMERIC,
                tax NUMERIC,
                availability INTEGER,
                number_of_reviews INTEGER
            )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        # Fecha a conexão ao final do processo
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # Insere o item no banco de dados
        try:
            self.cursor.execute("""
                INSERT INTO books (link, genre, title, image_url, description, upc, product_type, 
                                   price_excluding_tax, price_including_tax, tax, availability, number_of_reviews)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item['link'],
                item['genre'],
                item['title'],
                item['image_url'],
                item['description'],
                item['upc'],
                item['product_type'],
                item['price_excluding_tax'],
                item['price_including_tax'],
                item['tax'],
                item['availability'],
                item['number_of_reviews']
            ))

            self.connection.commit()

        except psycopg2.Error as e:
            spider.logger.error(f"Erro ao inserir no PostgreSQL: {e}")
            self.connection.rollback()
            raise DropItem(f"Erro ao inserir item no banco de dados: {e}")

        return item
