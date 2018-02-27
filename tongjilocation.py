#-*- coding:utf-8 -*-

from filereader import FileReader
from collections import Counter

def tongjilocation():
    filereader = FileReader("../1022.csv")
    attridx = filereader.getattridx("LOCATION")
    trandata = {}
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        loc = tmptran[attridx]
        try:
            locinfo = loc.split(";")[1].split("/")
            targetloc = locinfo[0]
            if targetloc not in trandata:
                trandata[targetloc] = 0
            trandata[targetloc] += 1
        except:
            print loc
            # raw_input()

    valuelist = trandata.values()
    valuelist.sort()
    c = Counter(valuelist)
    keylist = c.keys()
    keylist.sort()
    for key in keylist:
        print key,"\t:\t",c[key]
        raw_input()
    raw_input()
    itemslist = trandata.items()
    itemslist.sort(key=lambda v:v[1],reverse=True)
    for key,value in itemslist:
        print key
        print value
        raw_input()

    # print valuelist

if __name__ == "__main__":
    tongjilocation()