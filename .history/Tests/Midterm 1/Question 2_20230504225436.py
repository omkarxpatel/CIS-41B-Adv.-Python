from typing import NamedTuple

class GasConcentration(NamedTuple):
    gas: str
    pre_1750: str
    recent: str
    absolute_increase: str
    percentage_increase: str

class GasData:
    def __init__(self, data):
        self.data = data
    
    def __str__(self):
        return "\n".join([f"{i+1}. {g.gas}: Pre-1750: {g.pre_1750}, Recent: {g.recent}, Absolute increase since 1750: {g.absolute_increase}, Percentage increase since 1750: {g.percentage_increase}" for i, g in enumerate(self.data)])
    
    def __getitem__(self, key):
        return self.data[key]
    
    def sort_by_column(self, column):
        return GasData(sorted(self.data, key=lambda g: getattr(g, column)))
    
    def search_by_gas(self, gas):
        return GasData([g for g in self.data if g.gas.lower() == gas.lower()])



import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Greenhouse_gas"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
table = soup.find("table", class_="wikitable")

data = []
rows = table.find_all("tr")
for row in rows[1:]:
    cols = row.find_all("td")
    gas = cols[0].text.strip()
    pre_1750 = cols[1].text.strip()
    recent = cols[2].text.strip()
    absolute_increase = cols[3].text.strip()
    percentage_increase = cols[4].text.strip()
    data.append(GasConcentration(gas, pre_1750, recent, absolute_increase, percentage_increase))

# Create a GasData object and print the data
gas_data = GasData(data)
print(gas_data)

# Sort the data by the recent column and print the sorted data
sorted_gas_data = gas_data.sort_by_column("recent")
print(sorted_gas_data)

# Search for a specific gas and print the matching data
searched_gas_data = gas_data.search_by_gas("Methane")
print(searched_gas_data)
