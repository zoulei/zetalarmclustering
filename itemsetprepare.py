# -*- coding:utf-8 -*-
import time
import fpg
import os
import removeduplicate

def generateitemsetminingrawdata(secstep=60,datasize = 1.0):
    ifile = open("../cleandata")
    filesize = 0
    for line in ifile:
        filesize += 1
    ifile.close()
    ifile = open("../cleandata")


    datadict = {}
    rawdatadict= {}
    wrongcnt = 0
    notime = 0
    idx = 0
    limitsize= int(filesize * datasize)
    for line in ifile:
        idx += 1
        if idx > limitsize:
            break
        if idx % 1000000 == 0:
            print "generaterawdata:",idx
        try:
            alarmcode,nename,summary,happentime = line.strip().split("\t")
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
        warninfo = fpg.DistinctWarning(alarmcode,nename,summary)
        if key not in datadict:
            datadict[key] = []
        if warninfo not in datadict[key]:
            datadict[key].append(warninfo)
        if key not in rawdatadict:
            rawdatadict[key] = []
        rawdatadict[key].append(line)
    ifile.close()
    print "notime:",notime
    print "wrongcnt:",wrongcnt

    writefileflag = True
    if writefileflag:
        ofile = open("../itemmining", "w")
    keylist = datadict.keys()
    keylist.sort()
    idx = 0
    testfile = open("../testdata", "w")
    endflag = len(keylist) * 8 / 10
    for key in keylist:
        idx += 1
        if idx > endflag:
            testfile.write("".join(rawdatadict[key]))
        else:
            if writefileflag:
                ofile.write("\t".join([str(v) for v in datadict[key]])+"\n" )

    if writefileflag:
        ofile.close()
    testfile.close()

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
    fpgobj.tongjicause(datadict, 110000)
    fpgobj.save()

if __name__ == "__main__":
    # for step in [v*60 for v in [10,]]:
    start = 0
    for step in [v*60 for v in xrange(1,16)]:
        start = time.time()
        generateitemsetminingrawdata(step)
        print "gendata:::::::",step,time.time() - start
        start = time.time()
        fpgobj = fpg.FPGrowth("../itemmining")
        fpgobj.run()
        print "traintime:::::::",step,time.time() - start
        start = time.time()
        # fpgobj.save()
        # highestthre = fpgobj.gethighestrate()
        # for thre in [highestthre / 2, highestthre / 4, highestthre / 10]:
        #     fpgobj.clusterdata("../testdata",thre,step)
        fpgobj.clusterdata("../testdata", 0.5, step)
        print "time:::::::",step,time.time() - start

    start = 0
    for datasize in [v * 0.1 for v in xrange(1,11)]:
        start = time.time()
        generateitemsetminingrawdata(900,datasize)
        print "gendata:::::::",datasize,time.time() - start
        start = time.time()
        fpgobj = fpg.FPGrowth("../itemmining")
        fpgobj.run()
        print "traintime:::::::",datasize,time.time() - start
        start = time.time()
        # fpgobj.save()
        # highestthre = fpgobj.gethighestrate()
        # for thre in [highestthre / 2, highestthre / 4, highestthre / 10]:
        #     fpgobj.clusterdata("../testdata",thre,step)
        fpgobj.clusterdata("../testdata", 0, 900)
        print "time:::::::",datasize,time.time() - start



    # start = 0
    # for step in [v*60 for v in [15,]]:
    #     start = time.time()
    #     print "start:",start
    #     # generateitemsetminingrawdata(step)
    #     print "generatedataover"
    #     fpgobj = fpg.FPGrowth("../itemmining")
    #     fpgobj.run()
    #     print "traintime:::::::",step,time.time() - start
    #     start = time.time()
    #     # fpgobj.save()
    #     # highestthre = fpgobj.gethighestrate()
    #     # for thre in [highestthre / 2, highestthre / 4, highestthre / 10]:
    #     #     fpgobj.clusterdata("../testdata",thre,step)
    #     fpgobj.clusterdata("../testdata", 0, step)
    #     print "time:::::::",step,time.time() - start