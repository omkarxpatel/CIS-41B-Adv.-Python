from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re

class WebScraper:
    def __init__(self, htmlfile=None, htmlsite=None):
        self.htmlfile = htmlfile
        self.htmlsite = htmlsite
        
    def __repr__(self):
        return f"WebScraper(htmlfile={self.htmlfile}, htmlsite={self.htmlsite})"

    def __enter__(self):
        self.f = open(self.htmlfile, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
    
    def __call__(self):    
        html = urlopen(self.htmlsite)
        return BeautifulSoup(html, 'html.parser')    
    
    def soupf(self):
        soupf = self.__enter__()
        contents = self.f.read()
        soupf = BeautifulSoup(contents, 'html.parser')
        print(soupf.prettify()); print(soupf.h2); print(soupf.head); print(soupf.li); print("HTML: {0}, name: {1}, text: {2}".format(soupf.h2, soupf.h2.name, soupf.h2.text)); print(25*'=-')
        self.__exit__(None, None, None)
        return soupf
    
    def souph(self):
        souph = self.__call__()
        print(souph.prettify()); print(souph.h2); print(souph.head); print(souph.li); print("HTML: {0}, name: {1}, text: {2}".format(souph.h2, souph.h2.name, souph.h2.text)); print(25*'=-')
        return souph
    
    def children(self, html):
        [print(child.name) for child in html.recursiveChildGenerator() if child.name is not None]           

    def findAll(self, html, tags):
        dict = {}

        for tag in html.find_all(tags):
            print("{0}: {1}".format(tag.name, tag.text))
            r = re.compile(r'\s')
            s = r.split(tag.text)
            dict[s[0]] = s[1]

        for k,v in dict.items():
            print('key= ',k,'\tvalue= ',v)    

    def appendTag(self, html, tag, nustr):
        newtag = html.new_tag(tag)
        newtag.string=nustr
        ultag = html.ul  
        ultag.append(newtag)  

        print(ultag.prettify()) 

    def insertAt(self, html, tag, nustr, index):
        newtag = html.new_tag(tag)
        newtag.string = nustr
        ultag = html.ul   
        ultag.insert(index, newtag)   

        print(ultag.prettify()) 

    def selectIndex(self, html, index):
        soup = BeautifulSoup(html, 'html.parser')
        sel = soup.select(f'li:nth-of-type({index})')
        print(sel)

    def selectParagraph(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        p_elems = soup.find_all('p')
        print(p_elems)

        for
