import requests
from bs4 import BeautifulSoup
import json
import time

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

assessment_links = []

for link in links:

    href = link.get("href")

    if href and "product-catalog/view" in href:

        full_link = "https://www.shl.com" + href

        if full_link not in assessment_links:

            assessment_links.append(full_link)

all_assessments = []

for link in assessment_links:

    try:

        response = requests.get(link, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.text.replace(" | SHL", "")

        paragraphs = soup.find_all("p")

        description = ""

        for p in paragraphs:

            text = p.get_text(strip=True)

            if len(text) > 100:

                description = text

                break

        assessment_data = {
            "name": title,
            "url": link,
            "description": description
        }

        if description:

            all_assessments.append(assessment_data)

        print("Scraped:", title)

        time.sleep(1)

    except Exception as e:

        print("Error scraping:", link)

with open("data/assessments.json", "w") as file:

    json.dump(all_assessments, file, indent=4)

print("Data saved successfully")