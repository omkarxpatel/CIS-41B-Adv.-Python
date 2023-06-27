import pandas as pd
import requests
from collections import defaultdict
from typing import NamedTuple

from bs4 import BeautifulSoup

class GreenhouseGasData(NamedTuple):
   Gas: str
   Pre_1750: float
   Recent: str
   Absolute_increase_since_1750: str
   Percentage_increase_since_1750: str


class GreenhouseGasCollection:
   def __init__(self):
       self.data = []

   def __repr__(self):
       return str(self.data)

   def add_data(self, gas_data):
       self.data.append(gas_data)

   def sort_by(self, column):
       if column not in GreenhouseGasData._fields:
           raise ValueError(f"{column} not found in {GreenhouseGasData._fields}")
       
       self.data = sorted(self.data, key=lambda x: getattr(x, column))

   def search(self, gas):
       for gas_data in self.data:
           if gas_data.Gas == gas:
               return gas_data
           else:
               continue
           
       return None


class WebScraping:
   def __init__(self, url):
       self.url = url
       self.response = requests.get(self.url)
       self.soup = BeautifulSoup(self.response.text, 'html.parser')

   def extract_data(self):
       
       data = defaultdict(list)
       tables = self.soup.find_all('table', {'class': 'wikitable'})
       rows = tables[2].find_all('tr')[1:]
       
       for row in rows:
           cols = row.find_all('td')
           cols = [col.text.strip().replace("ppm", "").replace("ppb", "") for col in cols]
           cols = [col.split('[')[0].split('\xa0')[0] if '[' in col else col.split('\xa0')[0] for col in cols]

           data['Gas'].append(cols[0])
           data['Pre_1750'].append(float(cols[1]))
           data['Recent'].append(float(cols[2]))
           data['Absolute_Increase_Since_1750'].append(float(cols[3]))
           data['Percentage_Increase_Since_1750'].append((cols[4].rstrip('%')))

       return data



def main():
   ws = WebScraping('https://en.wikipedia.org/wiki/Greenhouse_gas')
   data = ws.extract_data()
   collection = GreenhouseGasCollection()

   for i in range(len(data['Gas'])):
       gas_data = GreenhouseGasData(data['Gas'][i], data['Pre_1750'][i], data['Recent'][i], data['Absolute_Increase Since 1750'][i], data['Percentage Increase Since 1750'][i])
       collection.add_data(gas_data)

   dataframe = pd.DataFrame(collection.data, columns=GreenhouseGasData._fields)
   print("Dataframe:\n", dataframe)


main()