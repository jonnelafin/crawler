#!/usr/bin/env python3
#Written by Elias Eskelinen
import sys
import time


class item:
    name = ""
    values = []
    links = []
    def __init__(self, name1, values1, links):
        self.name = name1
        self.values = values1
        self.links = links
srcfile = "items.txt"
items = []

def flatten(all):
    com = []
    for i in all:
        com.append(i.name)
        for x in i.values:
            com.append(x)
    return com
def index(all, title):
    ij = 0
    for i in all:
        if len(i.values) > 0:
            for x in i.values:
                if x.lower == title.lower:
                    return ij
                ij = ij + 1
        else:
            if i.lower == title.lower:
                return ij
            ij = ij + 1
    raise "not found lol"
def count(all, title):
    c = 0
    for i in all:
        if i.name == title.lower:
            c = c + 1
        if len(i.values > 0):
            for v in i.values:
                if i.lower == title.lower:
                    c = c + 1
    return c
def score(link, all, spe=False):
    try:
        ind = index(all, link)
#        ind = all.index(link)
    except Exception as e:
        try:
            ind = index(all, "https://" + link)
#            ind = all.index("https://" + link)
        except Exception as e2:
            try:
                ind = index(all, "http://" + link)
#                ind = all.index("http://" + link)
            except Exception as e3:
                try:
                    ind = index(all, "http://" + link + "/")
 #                   ind = all.index("http://" + link + "/")
                except Exception as e4:
                    try:
                        ind = index(all, "https://" + link + "/")
#                        ind = all.index("https://" + link + "/")
                    except Exception as e5:
                        if spe:
                            print("Target not in index.")
                        return 0
    #score = all.count(str(ind))
    score = count(all, str(ind))
    return score
def ref(all):
    f = []
    c = 0
    for i in all:
        if len(i.values) > 0:
            for x in i.values:
                c = c + 1
                try:
                    print( int(x) )
                    f.append(x)
                except Exception as e:
                    e = ""
        try:
            print( int(x.name) )
            f.append(x.name)
        except Exception as e:
            e = ""
        c = c + 1
    print(str(c) + " entries prosessed, " + str(len(f)) + " matching entries found.")
    return f
def cls():
    print("\033[H\033[J")
def load(quiet = True):
    global srcfile, items
    items = []
    with open(srcfile, "r+") as f:
        f2 = f.readlines()
        name = ""
        values = []
        links = []
        tc = 0
        vc = 0
        ttc = 0
        if not quiet:
            print("Loading file:")
            print("-------------")
        for i in f2:
            f3 = i.replace("\n","")
            #print(f3)
            if len(f3) > 0:
                if f3[0] == "    ":
                    ind = 1
                    if f3.find(":-") == -1:
                        ind = 0
                    values.append(f3.replace("    ","").split(":-")[0])
                    links.append(f3.replace("      ","").split(":-")[ind])
                    tc = tc + 1
                else:
                    vc = vc + 1
                    if name != "":
                        ttc = ttc + len(values)
                        items.append(item(name, values, links))
                    name = f3
                    values = []
                    links = []
        if name != "":
            items.append(item(name, values, []))
        f.close()
        if not quiet:
            print(str(vc) + " fields found")
            print(str(tc) + " values (tabs) found")
            print(str(ttc) + " values recorded \"passing by\"")
            print(str(len(items)) + " items in total")
            print("------------")
    return items
def search(query, items2=[]):
    global items
    if items2 == []:
        items2 = items
    results = []
    inp = []
    done = []
#    for i in items:
#        inp.append(i.name)
#        for x in i.values:
    ind = 0
    al = len(items2)
    for i in items2:
        ind = ind + 1
        print("Searching... " + str(ind) + " / " + str(al),end="\r")
        if i.name.upper().find(query.upper()) != -1 and (i not in done):
            results.append(item(i.name, i.values, []))
            done.append(i)
        for x in i.values:
            v = []
            if x.upper().find(query.upper()) != -1 and (x not in done):
#                results.append(i)
                v.append(x)
                done.append(x)
            if len(v) > 0:
                results.append(item(i.name, v, []))
    print()
    return results
def throwIDErr():
    raise ValueError("Proper authentication needed as an argument")
def test(times = -1):
    from random import randint
    import time
    items = []
    rounds = times
    if times == -1:
        rounds = int(input("How many items?\n>"))
    print("Testing with " + str(rounds) + " rounds...")
    for i in range(rounds):
        #print("--- %s seconds ---" % (time.time() - start_time),end="\r")
        name = ""
        values = []
        for x in range(randint(3,9)):
            name = name + str(randint(0, 9))
        if randint(0,5) == 3:
            for z in range(randint(2,5)):
                values.append(str(randint(0,200)))
        links = []
        ite = item(name, values, links)
        items.append(ite)
    all = 0
    print()
    #print("Made up the items!")
    start_time = time.time()
    print("........--- %s seconds ---" % (time.time() - start_time),end="\r")
    for i in range(rounds):
        print("--- %s seconds ---" % int(time.time() - start_time) + "[" + str(int(100-(rounds-i)/100)) + "%]                               ",end="\r")
        all = all + len(search(str(i), items))
    print("........--- %s seconds ---" % (time.time() - start_time))
    print(str(all) + " items found")
    if times == -1:
        input("press enter to continue\n")
def run(id):
    print("Welcome " + id["name"])
    time.sleep(1)
    load()
    print(str( len(items) ) + " items loaded:")
#    for i in items:
#        print(i.name)
#        for x in i.values:
#            print("        " + str(x))
#    print("You can quit anytime by typing \"!q\" as the search query")
    exit = False
    q = "-------------------------------------------------------------------------"
#    q = input("Search\n>")
    while not exit:
        cls()
        print("SEARCH")
#        print(str( len(items) ) + " items loaded.")
        print("You can quit anytime by typing \"!q\" as the search query")
        res = search(q)
        for i in res:
            print("Item name: " + i.name)
            print("Item values: ")
            for x in i.values:
                print("        " + str(x) + " : ")
            print("---------")
        print(str(len(res)) + " results.")
        q = input(">")
        if q == "!q":
            exit = True
        if q == "!test":
            test()
        if q == "!t":
            test(1)
            test(10)
            test(100)
            test(1000)
            test(10000)
            input("press enter to continue")
        if q == "!s":
            l = input("Term/link: ")
            print(str(l) + " has a score of " + str(score(l, items, True)))
            input("Press enter to continue.")
        if q == "!n":
            ref(items)
            input("Press enter to continue.")
        if q == "!f":
            f = flatten(items)
            print("Norm len: " + str(len(items)) + ", flat len: " + str(len(f)))
            input("Press enter to continue.")
if __name__ == "__main__":
    run({"name":"guest"})
