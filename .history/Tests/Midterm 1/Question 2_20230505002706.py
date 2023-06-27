# import requests
# from bs4 import BeautifulSoup
# from collections import namedtuple

# class GasConcentrationData:
#     GasTuple = namedtuple('GasTuple', ['Gas', 'Pre_1750', 'Recent', 'Absolute_increase_since_1750', 'Percentage_increase_since_1750'])
#     gas_data = []

#     def __init__(self, gas_list):
#         for gas in gas_list:
#             if len(gas) == 5:
#                 gas_tuple = self.GasTuple(*gas)
#                 self.gas_data.append(gas_tuple)

#     def __str__(self):
#         gas_str = ''
#         for gas in self.gas_data:
#             gas_str += f'{gas.Gas}: {gas.Recent}\n'
#         return gas_str

#     def search_gas(self, gas_name):
#         for gas in self.gas_data:
#             if gas.Gas.lower() == gas_name.lower():
#                 return gas
#         return None

#     def sort_gas(self, sort_column):
#         self.gas_data = sorted(self.gas_data, key=lambda x: getattr(x, sort_column.lower()))

# url = 'https://en.wikipedia.org/wiki/Greenhouse_gas'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# tables = soup.find_all('table', {'class': 'wikitable'})
# table = tables[2]
# rows = table.find_all('tr')
# gas_list = []


# for row in rows[1:]:
#     cols = row.find_all('td')
#     cols = [col.text.strip().replace("ppm", "").replace("ppb", "") for col in cols]
#     cols = [col.split('[')[0].split('\xa0')[0] if '[' in col else col.split('\xa0')[0] for col in cols]

#     gas_list.append(cols)

# gas_list = [[col[0]] + col[1::] for col in gas_list]

# print(gas_list)





# print()
# print()
# print()
# print()




from typing import NamedTuple


class GreenhouseGasData(NamedTuple):
    Gas: str
    Pre_1750: float
    Recent: float
    Absolute_increase_since_1750: float
    Percentage_increase_since_1750: float

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
        GreenhouseGasData("Carbon dioxide", gas_list[0][0], gas_list[0][1], gas_list[0][2], gas_list[0][3]),
        GreenhouseGasData("Methane", 722, 1874.0, 1152.0, 159.0),
        GreenhouseGasData("Nitrous oxide", 270, 329.0, 59.0, 21.9),
        GreenhouseGasData("Fluorinated gases", 0.5, 13.0, 12.5, 2500.0),
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