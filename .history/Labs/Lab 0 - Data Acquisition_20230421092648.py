    """_summary_

    Returns:
        _type_: _description_
    """
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

d = defaultdict(dict)

def get_values():
    rs = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita').content, 'html.parser').find('table', {'class': 'wikitable sortable'}).find_all('tr')[1:]

    for r in rs:
        cs = r.find_all('td')
        d[cs[0].text.strip()]['1980'], d[cs[0].text.strip()]['2018'] = cs[1].text.strip(), cs[14].text.strip()
    
def change_len(value):
    if value == "..":
        return "... "
    if len(value) == 3:
        return value+" "
    return value

def print_table():
    print("--------------------------------------------------------------")
    print("|                 Country Name                 | 1980 | 2018 |")
    print("--------------------------------------------------------------")
    for country in d:
        v1, v2 = d[country].get("1980"), d[country].get("2018")

        v1 = change_len(v1)
        v2 = change_len(v2)

        c1 = (45-len(country))*" "
        val = f"| {country}{c1}| {v1} | {v2} |"
        print(val)
        
    print("--------------------------------------------------------------")
    
def main():
    get_values()
    print_table()
    

main()