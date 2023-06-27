# Scrape, using Regex, all the <li> data on the local webpage 'Index.html' in the Webscraping Module on Canvas. Read the file as plain text.

import re

with open("Files/index.html", "r") as f:
    text = f.read()

lis = re.findall(r"<li>(.*?)</li>", text)

print(lis)
