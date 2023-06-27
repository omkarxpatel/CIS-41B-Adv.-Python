from collections import namedtuple

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

# Create named tuples for each row of data
data = [
    GasConcentration(*[cell.text.strip() for cell in row.find_all('td')])
    for row in rows
]

# Create a GasConcentrationData object to manage the data
gas_concentration_data = GasConcentrationData(data)
