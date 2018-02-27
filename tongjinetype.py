#-*- coding: utf-8 -*-

from filereader import FileReader
from collections import Counter

def tongjinetype():
    filereader = FileReader("../NE_INFO.csv")
    attridx = filereader.getattridx("NE_CAT_ID")
    trandata = {}
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        summary = tmptran[attridx]
        if summary not in trandata:
            trandata[summary] = 0
        trandata[summary] += 1
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(trandata)

    # valuelist = trandata.values()
    # valuelist.sort()
    # c = Counter(valuelist)
    # keylist = c.keys()
    # keylist.sort()
    # for key in keylist:
    #     print key,"\t:\t",c[key]
    #
    # itemslist = trandata.items()
    # itemslist.sort(key=lambda v:v[1],reverse=True)
    # for key,value in itemslist:
    #     print key
    #     print value
    #     raw_input()

    # print valuelist

if __name__ == "__main__":
    tongjinetype()
