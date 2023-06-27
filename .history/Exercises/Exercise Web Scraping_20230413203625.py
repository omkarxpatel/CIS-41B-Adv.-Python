# Write a Python script to scrape this website:

# https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capitaLinks to an external site.

# Scrape the "Production-based emissions: annual carbon dioxide emissions in metric tons per capita" for the data.  Use the functionality of Beautifulsoup to scrape the data. 
# Scrape the columns:  "Country Name","1980","2018".  Store the scraped data in a defaultdict.
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

rs = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita').content, 'html.parser').find('table', {'class': 'wikitable sortable'}).find_all('tr')[1:]
d = defaultdict(dict)

for r in rs:
    cs = r.find_all('td')
    d[cs[0].text.strip()]['1980'], d[cs[0].text.strip()]['2018'] = cs[1].text.strip(), cs[4].text.strip()

print("----------------------------------------------------------")
print("|               Country Name               | 1980 | 2018 |")
print("----------------------------------------------------------")

def change_len(v)

for country in d:
    v1, v2 = d[country].get("1980"), d[country].get("2018")

    v1 += " " if len(v1) in [2,3] else ""


    
    v2 += " " if len(v2) in [2,3] else ""
    
    c1 = (41-len(country))*" "
    val = f"| {country}{c1}| {v1} | {v2} |"
    print(val)

print("----------------------------------------------------------")