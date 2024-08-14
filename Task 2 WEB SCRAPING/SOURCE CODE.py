import requests           
from bs4 import BeautifulSoup 
import csv 

# Step 1: Define the URL of the website to scrape
url = 'https://books.toscrape.com/'

# Step 2: Send a GET request to the website
response = requests.get(url)

# Step 3: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Step 4: Find the container that holds the book information
books = soup.find_all('article', class_='product_pod')

# Step 5: Extract the desired data
book_data = []
for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    availability = book.find('p', class_='instock availability').text.strip()
    
    book_data.append([title, price, availability])

# Step 6: Save the data to a CSV file
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Availability'])  # Write the header
    writer.writerows(book_data)

print("Data has been saved to books.csv")
