# -*- coding:utf-8 -*-
import time

def generateitemsetminingrawdata(secstep=60):
    ifile = open("../cleandata")
    datadict = {}
    wrongcnt = 0
    notime = 0
    for line in ifile:
        try:
            alarmcode,nename,happentime = line.strip().split("\t")
        except KeyboardInterrupt:
            raise
        except:
            notime += 1
            # print line
            continue

        try:
            timesec = time.mktime( time.strptime(happentime,"%Y/%m/%d %H:%M:%S") )
        except:
            wrongcnt += 1
            continue
        key = int(timesec) / secstep
        if key not in datadict:
            datadict[key] = []
        datadict[key].append(alarmcode)
    ifile.close()
    print "notime:",notime
    print "wrongcnt:",wrongcnt

    ofile = open("../itemmining","w")
    for key in datadict:
        ofile.write(" ".join(datadict[key])+"\n" )
    ofile.close()

if __name__ == "__main__":
    generateitemsetminingrawdata()