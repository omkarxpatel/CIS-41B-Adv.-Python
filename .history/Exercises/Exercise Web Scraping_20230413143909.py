# Write a Python script to scrape this website:

# https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capitaLinks to an external site.

# Scrape the "Production-based emissions: annual carbon dioxide emissions in metric tons per capita" for the data.  Use the functionality of Beautifulsoup to scrape the data. 
# Scrape the columns:  "Country Name","1980","2018".  Store the scraped data in a defaultdict.

import requests
from bs4 import BeautifulSoup
from collections import defaultdict

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'class': 'wikitable sortable'})
data = defaultdict(dict)


rows = table.find_all('tr')[1:]
for row in rows:
    cols = row.find_all('td')
    country = cols[0].text.strip()
    data[country]['1980'], data[country]['2018'] = cols[1].text.strip()
    data[country]['2018'] = cols[4].text.strip()

for country in data:
    print(country, data[country])