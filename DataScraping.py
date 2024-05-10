import os
import requests
from bs4 import BeautifulSoup
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

def scrape_books(url, page_count=0, max_pages=25):

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        titles = soup.find_all('h3')
        book_titles = [title.a['title'] for title in titles]

        prices = soup.find_all(class_='price_color')
        book_prices = [price.get_text() for price in prices]

        ratings = soup.find_all(class_='star-rating')
        book_ratings = [rating['class'][1] for rating in ratings]

        images = soup.find_all('img', class_='thumbnail')
        book_images = [image['src'] for image in images]

        availabilities = soup.find_all(class_='availability')
        book_availabilities = [availability.get_text().strip() for availability in availabilities]

        output_file = os.path.join('data_buku.csv') 
        with open(output_file, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Judul', 'Harga', 'Rating', 'Gambar', 'Ketersediaan']) 
            for i in range(len(book_titles)):
                writer.writerow([book_titles[i], book_prices[i], book_ratings[i], book_images[i], book_availabilities[i]])

        page_count += 1

        if page_count < max_pages:
            next_page = soup.find('li', class_='next')
            if next_page:
                next_page_url = next_page.a['href']
                next_page_url = '/'.join(url.split('/')[:-1]) + '/' + next_page_url
                scrape_books(next_page_url, page_count, max_pages)
    else:
        print("Gagal mengambil halaman:", response.status_code)

base_url = 'https://books.toscrape.com/catalogue/'
starting_page = 'page-1.html'
scrape_books(base_url + starting_page, max_pages=1)