import re
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Greenhouse_gas'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all('table', {'class': 'wikitable'})
table = tables[2]
rows = table.find_all('tr')
gas_list = []

for row in rows[1:]:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    cols[0] = re.sub(r'\[[0-9]+\]', '', cols[0])
    cols[1] = int(re.sub(r'[^\d]', '', cols[1]))
    cols[2] = re.sub(r'\[[0-9]+\]', '', cols[2])
    cols[3] = re.sub(r'\[[0-9]+\]', '', cols[3])
    cols[4] = re.sub(r'\[[0-9]+\]', '', cols[4])
    gas_list.append(cols)

gas_list = [[col[0]] + col[1::] for col in gas_list]
print(gas_list)