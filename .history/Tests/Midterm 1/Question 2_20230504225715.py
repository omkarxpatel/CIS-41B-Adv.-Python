from collections import namedtuple
import requests
from bs4 import BeautifulSoup


GasConcentration = namedtuple('GasConcentration', [
    'gas',
    'pre_1750',
    'recent',
    'absolute_increase',
    'percentage_increase',
])

class GasConcentrationData:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return '\n'.join(
            f'{d.gas}: {d.pre_1750} -> {d.recent} ({d.absolute_increase}, {d.percentage_increase}%)'
            for d in self.data
        )

    def sort_by_column(self, column):
        return GasConcentrationData(sorted(self.data, key=lambda d: getattr(d, column)))

    def search_by_gas(self, gas):
        return GasConcentrationData([d for d in self.data if d.gas.lower() == gas.lower()])



url = 'https://en.wikipedia.org/wiki/Greenhouse_gas'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', class_='wikitable sortable')
rows = table.tbody.find_all('tr')[1:]

data = [
    GasConcentration(*[cell.text.strip() for cell in row.find_all('td')])
    for row in rows
]

gas_concentration_data = GasConcentrationData(data)


sorted_data = gas_concentration_data.sort_by_column('recent')
print(sorted_data)

searched_data = gas_concentration_data.search_by_gas('carbon dioxide')
print(searched_data)
