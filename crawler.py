#!/usr/bin/env python3
#pip install requests for installation

print("Crawler.py By Jonnelafin")

print("Importing libraries...",end="\r")
import os
from bs4 import BeautifulSoup, SoupStrainer
import requests
import json 
print("Importing libraries DONE")

filename = "out.json"

def genList(reg, inden, sel):
    out = ""
    ind = inden + 1
    if type(sel) is list:
        for i in sel:
            out = out + genList(reg, ind, i)
    else:
        out = out + "\t"*ind + str(sel) + "\n"
    return out
def save(reg):
    global filename
    y = json.dumps(reg)
    with open(filename, "w+") as f:
        f.write(y)
        f.close()
    inden = 0
    with open("items.txt", "w+") as f2:
        out = "items:\n"
        out = genList(reg, -2, reg)
#        for i in reg:
#            if type(i) is list:
#                for i2 in i:
#                    out = out + "\t"*1 + i2 + "\n"
#            else:
#                out = out + "\t"*0 + i + "\n"
##            out = out + i + "\n"
        f2.write(out)
        f2.close()
def load():
    global filename
    out = []
    if not os.path.exists(filename):
        with open(filename, "w+") as n:
            n.write("")
            n.close()
    with open(filename, "r") as f:
        out = json.loads(f.read())
        f.close()
    return list(out)
def crawl(url, done=[], depth=0, depthmax=1):
    errors = 0
    count = 0
    skip = 0
    print("Crawling \"" + url + "\"..." + " "*40, end="\r")
    out = []
    if depth > depthmax:
        print("Crawling \"" + url + "\" MAX" + " "*40, end="\r")
        return [[], 0, 1, 0]
    if url in done:
        print("Crawling \"" + url + "\" SKIP" + " "*40, end="\r")
        return [done.index(url), 0, 1, 1]
    try:
        page = requests.get(url)    
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")
        for link in soup.find_all('a'):
    #        print(link.get('href'))
            url2 = link.get('href')
            if (not(url2 is None)) and url != url2 and len(url2) > 0 and url2[0] != "#":
                if url2[0] == "/" and url2[1] == "/":
                    url2 = "http:" + url2
                elif len(url2) > 0 and url2[0] == "/":
                    url2 = url + url2
                craw = crawl(url2, out, depth+1, depthmax)
                out.append(url2)
                if craw[0] != []:
                    out.append(craw[0])
                errors = errors + craw[1]
                count = count + craw[2]
                skip = skip + craw[3]
                if depth == 0:
                    save(out)
        print("Crawling \"" + url + "\" DONE " + " "*40, end="\r")
        out.append(url)
    except Exception as e:
        print("Crawling \"" + url + "\" ERR  " + " "*40, end="\r")
        print(e)
        return [[], 1, 1, 0]
    return [out, errors, count, skip]
if __name__ == "__main__":
    al = crawl("https://fi.wikipedia.org/", load())
    print()
    for i in al[0]:
        print(i)
    print("Indexed " + str(al[2]) + " sites with " + str(al[1]) + " errors and " + str(al[3]) + " skips.")
    print("Final index size: " + str(len(al[0])) + " entries.")