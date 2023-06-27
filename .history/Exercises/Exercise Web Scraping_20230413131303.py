# Write a Python script to scrape this website:

# https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capitaLinks to an external site.

# Scrape the "Production-based emissions: annual carbon dioxide emissions in metric tons per capita" for the data.  Use the functionality of Beautifulsoup to scrape the data. 
# Scrape the columns:  "Country Name","1980","2018".  Store the scraped data in a defaultdict.


import requests
from bs4 import BeautifulSoup
from collections import defaultdict

# Send a request to the website and get the HTML content
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita'
response = requests.get(url)
html_content = response.content

# Parse the HTML content using Beautifulsoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table that contains the required data
table = soup.find('table', {'class': 'wikitable sortable'})

# Create a defaultdict to store the scraped data
data_dict = defaultdict(dict)

# Find the header row of the table and extract the required columns
header_row = table.find('tr')
headers = [header.text.strip() for header in header_row.find_all('th')[1:4]]

# Find all rows of the table and extract the required data
for row in table.find_all('tr')[1:]:
    columns = row.find_all('td')
    country_name = columns[0].text.strip()
    data_dict[country_name][headers[0]] = columns[1].text.strip()
    data_dict[country_name][headers[1]] = columns[4].text.strip()
    data_dict[country_name][headers[2]] = columns[6].text.strip()

# Print the scraped data
print(data_dict)
