from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import numpy as np
import requests
import shutil
import sys


class CarbonEmissionsScraper:
    def __init__(self, url):
        self.url=url

    def openHtmlFile(self):
        f = open(self.url, "r")
        contents = f.read()
        return BeautifulSoup(contents, 'html.parser')

    def openHtmlSite(self):
        html = urlopen(self.url)
        return BeautifulSoup(html, 'html.parser')

    def children(self):
        [print(child.name) for child in (self.url).recursiveChildGenerator() if child.name is not None]

    def findAll(self,tags):
        dict = {}
        for tag in (self.url).find_all(tags):
            print("{0}: {1}".format(tag.name, tag.text))
            r = re.compile(r'\s')
            s = r.split(tag.text)
            dict[s[0]] = s[1]
        for k,v in dict.items():
            print('key= ',k,'\tvalue= ',v)

    def appendTag(self,tag,nustr):
        newtag = soupf.new_tag(tag)
        newtag.string=nustr
        ultag = soupf.ul
        ultag.append(newtag)
        print(ultag.prettify())

    def selectIndex(self, index):
        sel = "li:nth-of-type(" + str(index) + ")"
        print((self.url).select(sel))

    def selectParagraph(self):
        spanElem = (self.url).select('p')
        print(spanElem)
        for i in range(0, len(spanElem)):
            print(str((spanElem)[i]))

    def scrapeData(self,soup):
        table = soup.find('table', {'class': 'wikitable sortable'})
        data = defaultdict(list)

        table_rows = table.find_all('tr')

        scrape_index = []

        for index, item in enumerate(table_rows[0].find_all('th')):
            if "1980" in item.text or "2018" in item.text:
                scrape_index.append(index)

        # Iterate over the rows of the table
        for row in table_rows[1:]:
            cells = row.find_all('td')
            if len(cells) > 0:
                country_name = cells[0].text.strip()
            for index in scrape_index:
                data[country_name].append(cells[index].text.strip())
        return data
    
def main():
    url='https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita'
    response=CarbonEmissionsScraper(url)
    soup = response.openHtmlSite()
    data=response.scrapeData(soup)

    print(data)
if __name__ == "__main__":
    main()