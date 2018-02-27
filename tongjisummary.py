from filereader import FileReader
from collections import Counter
import time
import re

def tongjisummarydata():
    filereader = FileReader("../1022.csv")
    attridx = filereader.getattridx("LOCATION")
    trandata = {}
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        summary = tmptran[3]
        if summary not in trandata:
            trandata[summary] = [0,tmptran[attridx]]
        trandata[summary][0] += 1
    valuelist = [v[0] for v in trandata.values()]
    valuelist.sort()
    c = Counter(valuelist)
    keylist = c.keys()
    keylist.sort()
    for key in keylist:
        print key,"\t:\t",c[key]

    itemslist = trandata.items()
    itemslist.sort(key=lambda v:v[1][0],reverse=False)
    for key,value in itemslist:
        print key
        print "--------------------------------------------------------"
        print value[1]
        print "======================================================="
        raw_input()

    # print valuelist

def tongjifirstword():
    filereader = FileReader("../1022.csv")
    attridx = filereader.getattridx("SUMMARY")
    trandata = {}
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        summary = tmptran[attridx]
        summary = summaryprocesser(summary)
        summary = summary.strip()
        firstspace = summary.find(" ")
        if firstspace == -1:
            target = summary
        else:
            target = summary[:firstspace]
        if target not in trandata:
            trandata[target] = 0
        trandata[target] += 1

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(trandata)

def summaryprocesser(summary):
    replacelist = [",","\"",";","\r\n","\n",":","=","(",")","{","}"]
    summary = summary.lower()
    for symbol in replacelist:
        summary = summary.replace(symbol," ")
    return summary

def retrivetempleteinput():
    filereader = FileReader("../1022.csv")
    attridx = filereader.getattridx("SUMMARY")
    ofile = open("../input.dat","w")
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        summary = tmptran[attridx]
        # print summary
        # print "-------------------------------------------------------------"
        summary = summaryprocesser(summary)
        # print summary
        # print "=============================================================="
        # raw_input()
        ofile.write(summary+"\n")
    ofile.close()

def printsummary():
    filereader = FileReader("../1022.csv")
    attridx = filereader.getattridx("SUMMARY")
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        summary = tmptran[attridx]
        summary = summaryprocesser(summary)
        summary = summary.strip()
        if summary.startswith("an") and summary[7] == "a" and summary[8] == "n":
            print summary
            # raw_input()
            # time.sleep(3)

def testan():
    f = open("tongjisummary")
    pattern = "an[\w]{4}-an[\w]{4} [\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}"
    wordcontent = {}
    for line in f:
        line = line.strip()
        searchresult = re.search(pattern,line)
        if not searchresult:
            print line
            raise
        content = searchresult.group(0)
        line = line.replace(content," ")
        if line not in wordcontent:
            wordcontent[line] = 0
        wordcontent[line] += 1
    import pprint
    pprint.pprint(wordcontent)
    print len(wordcontent)

    # re.search("[]")

def test():
    pattern = "an[\d]{4}-an[\d]{4} [\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}"
    searchresult = re.search(pattern,"an1112-an3523 193.168.112.111")
    if searchresult:
        print searchresult.group(0)
    else:
        raise

if __name__ == "__main__":
    # retrivetempleteinput()
    tongjifirstword()
    # printsummary()
    # testan()
    # test()