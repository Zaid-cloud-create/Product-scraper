

import requests
from bs4 import BeautifulSoup

from openpyxl import Workbook

url = "https://books.toscrape.com/catalogue/category/books/science_22/index.html"

# 1. Request page
try:
    r = requests.get(url)
    r.raise_for_status()
except requests.RequestException as e:
    print(f"Request error: {e}")
    exit()

# 2. Parse HTML
soup = BeautifulSoup(r.text, "html.parser")

# 3. Find all product containers
items = soup.find_all("article", class_="product_pod")

# 4. Create Excel file
wb = Workbook()
ws = wb.active
ws.title = "Products"

# Excel header
ws.append(["Title", "Price", "Image URL"])

# 5. Extract data from each product
for item in items:
    # Title
    title = item.h3.a["title"]

    # Price
    price = item.find("p", class_="price_color").get_text().strip()

    # Image URL
    img = item.find("img")["src"]
    img_url = "https://books.toscrape.com/" + img.replace("../", "")

    # Add row to Excel
    ws.append([title, price, img_url])

# 6. Save file
wb.save("products.xlsx")
print("Scraping complete! File saved as products.xlsx")
