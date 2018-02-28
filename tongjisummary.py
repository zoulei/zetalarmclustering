from filereader import FileReader
from collections import Counter
import time
import re
import json

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
    trandata = {}
    fnamelist = ["../10"+str(v)+".csv" for v in xrange(22,32)]
    for fname in fnamelist:
        filereader = FileReader(fname)
        attridx = filereader.getattridx("SUMMARY")

        pattern = "[\w]{6}-[\w]{6}.+[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}"
        while True:
            tmptran = filereader.readtransection()
            if tmptran is None:
                filereader.close()
                break
            summary = tmptran[attridx]
            searchresult = re.search(pattern,summary)
            if searchresult:
               continue
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
    json.dump(trandata,open("trandata","w"))
    return trandata
    # kvlist = trandata.items()
    # kvlist.sort(key=lambda v:v[1])
    # for k, v in kvlist:
    #     print k,"\t:\t",v

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
        elif summary.startswith("su") and summary[7] == "s" and summary[8] == "u":
            print summary
        elif summary.startswith("dz") and summary[7] == "d" and summary[8] == "z":
            print summary
        elif summary.startswith("lh") and summary[7] == "l" and summary[8] == "h":
            print summary

def printvc():
    filereader = FileReader("../1022.csv")
    attridx = filereader.getattridx("SUMMARY")
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        summary = tmptran[attridx]
        summary = summaryprocesser(summary)
        summary = summary.strip()
        if summary.startswith("vc"):
            print tmptran[attridx]

def printtu():
    filereader = FileReader("../1022.csv")
    attridx = filereader.getattridx("SUMMARY")
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        summary = tmptran[attridx]
        summary = summaryprocesser(summary)
        summary = summary.strip()
        if summary.startswith("tu12"):
            print tmptran[attridx]

def printinfodata():
    filereader = FileReader("../1022.csv")
    attridx = filereader.getattridx("SUMMARY")
    locationidx = filereader.getattridx("LOCATION")
    trandata = json.load(open("trandata"))
    startwordlist = trandata.keys()
    startwordlist = [v.encode("ascii") for v in startwordlist]
    startwordlist = [v for v in startwordlist if len(v)]
    print startwordlist
    filelist = [open(v,"w") for v in startwordlist]
    locfilelist = [open(v+"loc","w") for v in startwordlist]
    fnamelist = ["../10"+str(v)+".csv" for v in xrange(22,32)]
    for fname in fnamelist:
        print fname
        filereader = FileReader(fname)
        while True:
            tmptran = filereader.readtransection()
            if tmptran is None:
                filereader.close()
                break
            summary = tmptran[attridx]
            summary = summaryprocesser(summary)
            summary = summary.strip()
            for idx in xrange(len(startwordlist)):
                stword = startwordlist[idx]
                ofile = filelist[idx]
                locofile = locfilelist[idx]
            # for stword, ofile in zip(startwordlist,filelist):
                if summary.startswith(stword):
                    ofile.write(tmptran[attridx]+"\n")
                    locofile.write(tmptran[locationidx]+"\n")
                    break
    for v in filelist:
        v.close()

def testan():
    f = open("suxxxx-suxxxx")
    pattern = "[\w]{6}-[\w]{6}.+[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}"
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

def testvc():
    f = open("vcinfo")
    pattern = "VC.*?:BN:ME"
    wordcontent = {}
    for line in f:
        line = line.strip()
        searchresult = re.search(pattern,line)
        if not searchresult:
            print line
            raise
        content = searchresult.group(0)
        if content not in wordcontent:
            wordcontent[content] = 0
        wordcontent[content] += 1
    import pprint
    pprint.pprint(wordcontent)
    print len(wordcontent)

def test():
    pattern = "se.+se"
    searchresult = re.search(pattern,"se sdg_sdg sdg-1 se")
    if searchresult:
        print searchresult.group(0)
    else:
        raise

if __name__ == "__main__":
    # retrivetempleteinput()
    # tongjifirstword()
    # printsummary()
    # testan()
    # test()
    # printvc()
    # testvc()
    # printtu()
    printinfodata()
