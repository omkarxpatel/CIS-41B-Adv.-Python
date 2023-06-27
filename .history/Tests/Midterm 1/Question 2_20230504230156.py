import requests
from lxml import html
from collections import namedtuple

# Define the named tuple
GasConcentration = namedtuple('GasConcentration', [
    'gas',
    'pre_1750',
    'recent',
    'absolute_increase',
    'percentage_increase',
])

# Define the custom class
class GasConcentrationData:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return '\n'.join(
            f'{d.gas}: {d.pre_1750} -> {d.recent} ({d.absolute_increase}, {d.percentage_increase}%)'
            for d in self.data
        )

    def sort_by_column(self, column):
        # Implement sorting by a specific column using the `sorted` function
        return GasConcentrationData(sorted(self.data, key=lambda d: getattr(d, column)))

    def search_by_gas(self, gas):
        # Implement searching for a specific gas by filtering the data
        return GasConcentrationData([d for d in self.data if d.gas.lower() == gas.lower()])

# Scrape the data from the Wikipedia page
url = 'https://en.wikipedia.org/wiki/Greenhouse_gas'
response = requests.get(url)
tree = html.fromstring(response.content)
table = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody')[0]
rows = table.xpath('.//tr')[1:]

# Create named tuples for each row of data
data = [
    GasConcentration(*[cell.text.strip() if cell.text is not None else '' for cell in row.xpath('.//td')][:6])
    for row in rows
]


# Create a GasConcentrationData object to manage the data
gas_concentration_data = GasConcentrationData(data)



sorted_data = gas_concentration_data.sort_by_column('recent')
print(sorted_data)

searched_data = gas_concentration_data.search_by_gas('carbon dioxide')
print(searched_data)
