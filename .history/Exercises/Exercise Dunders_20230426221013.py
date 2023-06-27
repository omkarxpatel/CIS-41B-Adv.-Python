from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class WebScraper:
    def __init__(self, htmlfile=None, htmlsite=None):
        self.htmlfile = htmlfile
        self.htmlsite = htmlsite
        
    def __repr__(self): # unary
        return f"WebScraper(htmlfile={self.htmlfile}, htmlsite={self.htmlsite})"

    def __enter__(self): # unary
        self.f = open(self.htmlfile, "r")
        return self

    def __exit__(self, type, val, t): # binary
        self.f.close()
    
    def __call__(self):     # unary
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

        for elem in p_elems:
            print(str(elem))

def __len__(self):
    return 2

def __getitem__(self, key):
    if key == 'htmlfile':
        return self.htmlfile
    elif key == 'htmlsite':
        return self.htmlsite
    else:
        raise KeyError(f"{key} is not a valid key")
            

# scraper = WebScraper(htmlsite='https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita')