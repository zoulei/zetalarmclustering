from filereader import FileReader
import attributeparser

def printinfo():
    fnamelist = ["../10"+str(v)+".csv" for v in xrange(22,23)]
    cnt = 0
    found = 0
    wholeresult = {}
    # writefile = open("../cleandata","w")

    missloc = {}
    for fname in fnamelist:
        filereader = FileReader(fname)
        alarmcode = filereader.getattridx("ALARMCODE")
        attridx = filereader.getattridx("SUMMARY")
        locidx= filereader.getattridx("LOCATION")
        timeidx = filereader.getattridx("ALARMHAPPENTIME")
        cntidx = 0
        while True:
            tmptran = filereader.readtransection()
            cntidx += 1
            # print cntidx
            if tmptran is None:
                filereader.close()
                break

            summary = tmptran[attridx]
            location = tmptran[locidx]
            if location.startswith("SU6095-SU2551"):
                print "SUMMARY:"
                print summary
                print "--------------"
                print "LOCATION"
                print location

def printne():
    topo = attributeparser.TopoInfo(full=True)
    print topo.m_locdata[4408]
    print topo.m_locdata[4409]

    print topo.m_locdata[4410]

if __name__ == "__main__":
    printne()
    # printinfo()