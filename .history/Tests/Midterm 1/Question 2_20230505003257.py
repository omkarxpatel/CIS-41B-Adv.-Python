import requests
from bs4 import BeautifulSoup
from typing import NamedTuple


class GreenhouseGasData(NamedTuple):
    Gas: str
    Pre_1750: float
    Recent: str
    Absolute_increase_since_1750: str
    Percentage_increase_since_1750: str

class GreenhouseGasCollection:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def sort_by(self, column):
        if column not in GreenhouseGasData._fields:
            raise ValueError(f"{column} not found in {GreenhouseGasData._fields}")
        self.data = sorted(self.data, key=lambda x: getattr(x, column))

    def search(self, gas):
        for gas_data in self.data:
            if gas_data.Gas == gas:
                return gas_data
        return None


def main():

    url = 'https://en.wikipedia.org/wiki/Greenhouse_gas'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table', {'class': 'wikitable'})
    table = tables[2]
    rows = table.find_all('tr')
    gas_list = []

    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip().replace("ppm", "").replace("ppb", "") for col in cols]
        cols = [col.split('[')[0].split('\xa0')[0] if '[' in col else col.split('\xa0')[0] for col in cols]

        gas_list.append(cols)

    gas_list = [[col[0]] + col[1::] for col in gas_list]

    data = [
        GreenhouseGasData("Carbon dioxide", int(gas_list[0][1]), str(gas_list[0][2]), str(gas_list[0][3]), str(gas_list[0][4])),
        GreenhouseGasData("Methane", int(gas_list[1][1]), str(gas_list[1][2]), str(gas_list[1][3]), str(gas_list[1][4])),
        GreenhouseGasData("Nitrous oxide", int(gas_list[2][1]), str(gas_list[2][2]), str(gas_list[2][3]), str(gas_list[2][4])),
        GreenhouseGasData("Fluorinated gases", int(gas_list[3][1]), str(gas_list[3][2]), str(gas_list[3][3]), str(gas_list[3][4])),
    ]
    collection = GreenhouseGasCollection(data)
    print("Data:", collection)

    collection.sort_by("Recent")
    print("Data sorted by Recent:", collection)

    result = collection.search("Carbon dioxide")
    if result:
        print("Data for Carbon dioxide:", result)
    else:
        print("Data for Carbon dioxide not found")


if __name__ == "__main__":
    main()