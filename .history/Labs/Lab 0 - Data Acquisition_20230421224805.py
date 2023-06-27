from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re


class FileStream():

    def __init__(self, url):
        self.htmlsite = url
    
    
    def openHtmlSite(self):
        html = urlopen(self.htmlsite)
        return html
        
        
        
class Parser():

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
    
    
    def findData(self, column):
        tables = self.soup.find_all('table')
        table = self.soup.find('table', class_='wikitable sortable').tbody
        rows = table.find_all('tr')
        headers = table.findAll('th')
        
        #find all countries in the table
        Countries = []
        string = ""
        for row in rows:
            countries = row.findAll("a", href=True)
            if len(countries) > 1: #dealing with rows that have multiple countries
                for tag in countries:
                    if tag != countries[-1]:
                        string += tag.text + ", "
                    else:
                        string += tag.text
                Countries.append(string)
                string = ""
            elif len(countries) == 1: #dealing with rows that have only one country
                for tag in countries:
                    Countries.append(tag.text)
        Countries = Countries[2:]
        
        #clean column title strings to find data for any column
        #make sure that scraping is not hard coded for "2017 (% of world)" column
        headers = headers[5:]
        Headers = []
        for header in headers:
            header = str(header)              
            Headers.append(header)
        Headers = [x.replace('\n', '').replace('<br/>', ' ').replace('  ', ' ').replace('[22]', '').replace('[23]', '') 
                   for x in Headers]
        clean = re.compile('<.*?>')
        Headers = [re.sub(clean, '', x) 
                   for x in Headers]

        #get data for column "2017 (% of world)"
        columnIdx = Headers.index(column) + 1
        rows = rows[5:] #remove world and header rows
        columnData = []
        for row in rows:
            data = row.findAll('td')
            percent = re.findall('(?<=<td>)(.*?)(?=</td>)', str(data[columnIdx]))
            percent = percent[0]
            columnData.append(percent)

        return [Countries, columnData]
        
        
    
class Dictionary():
    
    def __init__(self, keysVals):
        self.keys = keysVals[0]
        self.vals = keysVals[1]
        
        
    def createDict(self):
        dictionary = defaultdict(str)
        index = 0
        for k in self.keys:
                dictionary[k] = self.vals[index]
                index += 1
        return dictionary
    
    
    
class OutputStream():
    
    def __init__(self, dictionary):
        self.d = dictionary
    
    
    def __str__(self):
        #output defaultdict as a table
        printing = " {:<45} |  {:<10}\n".format("COUNTRY", "DATA")
        printing += "-"*65 + "\n"
        for country, data in self.d.items():
            printing += " {:<45} |  {:<10}\n".format(country, data)      
        return printing



if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions"
    html = FileStream(url).openHtmlSite()
    data = Parser(html).findData('2017 (% of world)') #can find data for any column
    dictionary = Dictionary(data).createDict()
    print(dictionary)
    table = OutputStream(dictionary)
    print(table)

