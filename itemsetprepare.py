# -*- coding:utf-8 -*-
import time
import fpg
import os
import removeduplicate

def generateitemsetminingrawdata(secstep=60):
    ifile = open("../cleandata")
    datadict = {}
    wrongcnt = 0
    notime = 0
    idx = 0
    for line in ifile:
        idx += 1
        if idx % 1000 == 0:
            print idx
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
    keylist = datadict.keys()
    keylist.sort()
    for key in datadict:
        ofile.write(" ".join(datadict[key])+"\n" )
    ofile.close()

def tongjicause(secstep=60):
    ifile = open("../cleandata")
    datadict = {}
    wrongcnt = 0
    notime = 0
    idx = 0
    for line in ifile:
        idx += 1
        if idx % 1000 == 0:
            print "tongjicauseidx:",idx
        # if idx == 1000000:
        #     break
        try:
            alarmcode,nename,happentime = line.strip().split("\t")
        except KeyboardInterrupt:
            raise
        except:
            notime += 1
            continue

        try:
            timesec = time.mktime( time.strptime(happentime,"%Y/%m/%d %H:%M:%S") )
        except KeyboardInterrupt:
            raise
        except:
            wrongcnt += 1
            continue
        key = int(timesec) / secstep
        if key not in datadict:
            datadict[key] = {}
        if alarmcode not in datadict[key] or timesec < datadict[key][alarmcode]:
            datadict[key][alarmcode] = timesec

    ifile.close()
    print "notime:",notime
    print "wrongcnt:",wrongcnt

    fpgobj = fpg.FPGrowth("../itemmining")
    fpgobj.load()
    fpgobj.tongjicause(datadict,110000)
    fpgobj.save()

    # ofile = open("../itemmining","w")
    # for key in datadict:
    #     ofile.write(" ".join(datadict[key])+"\n" )
    # ofile.close()

if __name__ == "__main__":
    # generateitemsetminingrawdata()
    # removeduplicate.removedup()
    # os.system("head -n 110000 ../itemmining > ../itemmining110000")
    # os.system("head -n 11000 ../itemmining > ../itemmining11000")
    # os.system("cp ../itemmining ../itemminingbackup")
    # os.system("cp ../itemmining11000 ../itemmining")

    fpgobj = fpg.FPGrowth("../itemmining")
    fpgobj.run()
    fpgobj.save()
    fpgobj.load()
    tongjicause()
