from filereader import FileReader

def searchlocation(locstr):
    filereader= FileReader("../NE_INFO.csv")
    label = True
    while label:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        # for idx,v in enumerate(tmptran):
        #     if locstr in v:
        if locstr in tmptran:
            print "found",filereader.getattr( tmptran.index(locstr))
            print locstr
            # label = False
            break
    print "over"

def calneidlen():
    filereader= FileReader("../NE_INFO.csv")
    attridx = filereader.getattridx("NE_NO")
    lendict = {}
    idx = 0
    while True:
        tmptran = filereader.readtransection()
        if tmptran is None:
            break
        neid = tmptran[attridx]
        neidlen = len(neid)
        if neidlen not in lendict:
            lendict[neidlen] = 0
        lendict[neidlen] += 1
        idx += 1
        print neid
        if idx % 100 == 0:
            raw_input()
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lendict)

if __name__ == "__main__":
    searchlocation("DZ1067-LHDZ02_8G")
    searchlocation("DZ1062-DZ2406")
    searchlocation("SU6029-SU6037")
    searchlocation("56008")
    searchlocation("BN:ME{131366445}")
    searchlocation("SM2607_S1")

    # calneidlen()
