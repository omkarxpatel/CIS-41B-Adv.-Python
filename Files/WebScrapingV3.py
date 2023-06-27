'''

Install Beautiful Soup (BS4).
From command line type:
python -m pip install bs4

Install Matplotlib
From command line type:
python -m pip install matplotlib

Install shutil
From cmmand line type:
python -m pip install shutil

'''


from urllib.request import urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import requests
import shutil
import sys


def openHtmlFile(htmlfile):
    f = open(htmlfile, "r")
    contents = f.read()
    return BeautifulSoup(contents, 'html.parser')

def openHtmlSite(htmlsite):    
    html = urlopen(htmlsite)
    return BeautifulSoup(html, 'html.parser')    

soupf = openHtmlFile("index.html") #local file
print(soupf.prettify())
print(soupf.h2)
print(soupf.head)
print(soupf.li)
print("HTML: {0}, name: {1}, text: {2}".format(soupf.h2, soupf.h2.name, soupf.h2.text))
print(25*'=-')

souph = openHtmlSite('https://climate.nasa.gov/evidence/')
print(souph.prettify())
print(souph.h2)
print(souph.head)
print(souph.li)
print("HTML: {0}, name: {1}, text: {2}".format(souph.h2, souph.h2.name, souph.h2.text))
print(25*'=-')

# headers and lists
print(soupf.h2)
print(soupf.head)
print(soupf.li)
print("HTML: {0}, name: {1}, text: {2}".format(soupf.h2, soupf.h2.name, soupf.h2.text))
print(souph.h2)
print(souph.head)
print(souph.li)
print("HTML: {0}, name: {1}, text: {2}".format(souph.h2, souph.h2.name, souph.h2.text))
print(25*'=-')

# children
def children(html):
    [print(child.name) for child in html.recursiveChildGenerator() if child.name is not None]           

children(soupf)
children(souph)
print(25*'=-')

# find_all
def findAll(html,tags):
    dict = {}
    for tag in html.find_all(tags):
        print("{0}: {1}".format(tag.name, tag.text))
        r = re.compile(r'\s')
        s = r.split(tag.text)
        dict[s[0]] = s[1]
    for k,v in dict.items():
        print('key= ',k,'\tvalue= ',v)    

findAll(soupf,'td')
findAll(souph,'td')
print(25*'=-')
 
# append tag   
def appendTag(html,tag,nustr):
    newtag = soupf.new_tag(tag)
    newtag.string=nustr
    ultag = soupf.ul  
    ultag.append(newtag)  
    print(ultag.prettify()) 

appendTag(soupf,'li','First')
appendTag(souph,'li','First')
print(25*'=-')

# inserting a new tag at position
def insertAt(html,tag,nustr,index):
    newtag = html.new_tag(tag)
    newtag.string = nustr
    ultag = html.ul   
    ultag.insert(index, newtag)   
    print(ultag.prettify()) 
    
insertAt(soupf,'li','Second',2)
insertAt(souph,'li','Second',2)
print(25*'=-')

# select list element
def selectIndex(html,index):
    sel = "li:nth-of-type("+str(index)+")"
    print(html.select(sel))
    
selectIndex(soupf,3)
selectIndex(souph,3)
print(25*'=-')

# select paragraph
def selectParagraph(html):
    spanElem = html.select('p')
    print(spanElem)
    for i in range(0,len(spanElem)):
        print(str((spanElem)[i]))   
        
selectParagraph(soupf)
selectParagraph(souph)
print(25*'=-')

# select span
def selectSpan(html):
    spanElem = html.select('span')
    print(spanElem)
    for i in range(0,len(spanElem)):
        print(str((spanElem)[i]))    
        
selectSpan(soupf)
selectSpan(souph)
print(25*'=-')

def scrapefile():
    alink = "https://automatetheboringstuff.com/files/"
    page = requests.get(alink)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.select('a')
    htpfile = alink + links[20].text
    res = requests.get(htpfile)
    res.raise_for_status()
    playFile = open('RomeoAndJuliet.txt', 'wb')
    for chunk in res.iter_content(100000):
        print(chunk)
        playFile.write(chunk)
    playFile.close()
    
scrapefile()
print(25*'=-')
    
def scrapeimage():  
    wpage = 'https://www.livescience.com/37821-greenhouse-gases.html'
    htmldata = urlopen(wpage)
    soup = BeautifulSoup(htmldata, 'html.parser')
    images = soup.find_all('img')
    image1 = images[1]
    src = image1.attrs['src']
    req = requests.get(src, stream=True) 
    # end custom code
    if req.status_code == 200:  #200 status code = OK
        with open("image1.jpg", 'wb') as f: 
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, f)
    img = mpim.imread('image1.jpg')
    imgplot = plt.imshow(img)
    plt.show() 
    
scrapeimage()
