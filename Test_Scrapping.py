import os
import requests
from bs4 import BeautifulSoup
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

def scrape_quotes():
    url = 'https://quotes.toscrape.com/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        output_dir = 'hasil'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = os.path.join(output_dir, 'quotes_data.csv')

        with open(output_file, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Isi Quote', 'Author', 'Tags'])

            for quote in quotes:
                content = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()
                tags = ','.join([tag.get_text() for tag in quote.find_all('a', class_='tag')])

                writer.writerow([content, author, tags])

        print("Scraping data quotes selesai. Hasil tersimpan dalam file 'quotes_data.csv' di dalam folder 'data'.")
    else:
        print("Gagal", response.status_code)

scrape_quotes()
