![image](https://github.com/user-attachments/assets/149f1838-c3a0-4630-a7c1-78ab927ad83d)

📚 Books to Scrape - Web Scraping Project with Scrapy and PostgreSQL
This project uses Scrapy to extract book data from the website Books to Scrape. After the data is scraped, it is processed and stored in a PostgreSQL database for further analysis or integration with other tools.

🔧 Technologies Used: <br />
Python

Scrapy

PostgreSQL

📌 Features:
Extracts book information such as title, genre, price, description, availability, image, number of reviews, rating, and category.

Handles pagination to scrape all available books.

Cleans and processes the data before saving.

Stores structured data into a PostgreSQL database.

📁 Project Structure:
scrapy_project/: Contains the Scrapy spider and configuration.

pipelines.py: Processes and sends the data to PostgreSQL.

items.py: Defines the data fields to be scraped.

settings.py: Configures Scrapy behavior and database connection.

🚀 How to Run:
Clone the repository.

Set up your PostgreSQL database and update the connection settings.

Install dependencies: pip install -r requirements.txt

Run the spider: scrapy crawl books
