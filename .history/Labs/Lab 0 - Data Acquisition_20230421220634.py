"""
Lab 0 - Data Acquisition


Convert your script from Exercise Webscraping into a Python Class.  The Web scraping class encapsulates all the webscraping functions in the WebscrapingV3.py example file, except for the File and Image scraping functions.  Add appropriate dunders.  Review this website for creating and using class dunders:

https://www.geeksforgeeks.org/customize-your-python-class-with-magic-or-dunder-methods/?ref=lbpLinks to an external site.

If it's been a while since you programmed a Python Class, here is a video review on creating and using classes:

https://realpython.com/lessons/classes-python/Links to an external site.
"""
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.html = None
        self.soup = None
        self.table = None

    def __str__(self):
        return f"Url: {self.url}\nHtml: {self.html}\nSoup: {self.soup}\n Table: {self.table}"

    def open_html_site(self):
        self.html = urlopen(self.url)
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def openHtmlFile(htmlfile):
        f = open(htmlfile, "r")
        contents = f.read()
        return BeautifulSoup(contents, 'html.parser')

    def findAll(html, tags):
        dict = {}
        for tag in html.find_all(tags):
            print("{0}: {1}".format(tag.name, tag.text))
            r = re.compile(r'\s')
            s = r.split(tag.text)
            dict[s[0]] = s[1]
        for k, v in dict.items():
            print('key= ', k, '\tvalue= ', v)

    def appendTag(html, tag, nustr):
        newtag = soupf.new_tag(tag)
        newtag.string = nustr
        ultag = soupf.ul
        ultag.append(newtag)
        print(ultag.prettify())

    def insertAt(html, tag, nustr, index):
        newtag = html.new_tag(tag)
        newtag.string = nustr
        ultag = html.ul
        ultag.insert(index, newtag)
        print(ultag.prettify())

    def selectIndex(html, index):
        sel = "li:nth-of-type(" + str(index) + ")"
        print(html.select(sel))

    def get_table(self, table_class):
        self.table = self.soup.find('table', {'class': table_class})

    def selectParagraph(html):
        spanElem = html.select('p')
        print(spanElem)
        for i in range(0, len(spanElem)):
            print(str((spanElem)[i]))

    def selectSpan(html):
        spanElem = html.select('span')
        print(spanElem)
        for i in range(0, len(spanElem)):
            print(str((spanElem)[i]))