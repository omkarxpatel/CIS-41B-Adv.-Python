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
#     cols = [col.text.strip() for col in cols]
#     gas_list.append(cols)
# print(gas_list)








