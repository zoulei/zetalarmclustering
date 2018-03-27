# -*- coding:utf-8 -*-
import itertools
import json
import copy
import os
import time
import signal
import multiprocessing
import shelve
import attributeparser
import traceback

TRAIN = False

class DistinctWarning:
    def __init__(self, alarmcode = None, nename = None, warnstr = None):
        self.m_alarmcode = alarmcode
        self.m_nename = nename
        if warnstr:
            self.loadfromstr(warnstr)

    def loadfromstr(self,warnstr):
        spaceidx = warnstr.find(" ")
        self.m_alarmcode = warnstr[:spaceidx]
        self.m_nename = warnstr[spaceidx + 1:]

    def __str__(self):
        return self.m_alarmcode + " " + self.m_nename

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.m_alarmcode == other.m_alarmcode and self.m_nename == other.m_nename

class FPGrowth:
    def __init__(self,fname=None):
        self.m_fname = fname
        self.initdocname()
        self.m_itemsetsroot = {}
        self.m_topo = attributeparser.TopoInfo()

    def initdocname(self):
        self.m_length = 0
        ifile = open(self.m_fname)
        for line in ifile:
            self.m_length += 1

    def genreversemap(self):
        self.m_reversemap = {}
        print "gen reversemap"
        for key,value in self.m_tranmap.items():
            self.m_reversemap[value] = key
        print "over reversemap"

    def genmap(self):
        self.m_tranmap = {}
        transet = set()
        ifile = open(self.m_fname)
        idx = 0
        for line in ifile:
            idx += 1
            if idx % 1000 == 0:
                print "genmap:",idx
            data = line.strip().split("\t")
            for v in data:
                transet.add(DistinctWarning(warnstr = v))
        print "len transet:",len(transet)
        for idx,v in enumerate(list(transet)):
            self.m_tranmap[v] = idx
        ifile.close()
        print "tranmap gen over"
        self.genreversemap()

    def run(self):
        # self.genmap()
        jsontranmap = json.load(open("fpgtranmap"))
        self.m_tranmap = {}
        for key,value in jsontranmap.items():
            self.m_tranmap[DistinctWarning(warnstr=key)] = value
        itemlen = len(self.m_tranmap)
        # itemlen = 100
        # if os.path.exists("fpgitemsets"):
        #     os.remove("fpgitemsets")
        # self.m_itemsets = shelve.open("fpgitemsets","c")
        # for idx in xrange(itemlen):
        #     print "genmap:",idx
        #     self.m_itemsets[str(idx)] = {}
        #     keylist = range(idx + 1,itemlen)
        #     valuedict = dict(zip([str(v) for v in keylist],[0]*len(keylist)))
        #     self.m_itemsets[str(idx)] = valuedict
        # self.m_itemsets.close()
        # os.system("cp fpgitemsets fpgitemsetsbackup")
        # return
        # os.system("cp fpgitemsetsbackup fpgitemsets")
        # self.m_itemsets = shelve.open("fpgitemsets")

        ifile = open(self.m_fname)
        idx = 0
        alllinelist = []
        linelist = []
        for line in ifile:
            linelist.append(line)
            idx += 1
            if idx % 1000 == 0:
                print idx
            if idx % 1500 == 0:
                alllinelist.append(linelist)
                linelist = []
        alllinelist.append(linelist)
        print "endreadfile"

        ofile = open("../pairdata","w")
        for linelist in alllinelist:
            start = time.time()
            print "start async",start
            datalist = self.async(linelist)
            print "end async",time.time() - start
            idx = 0
            for data in datalist:
                idx += 1
                if idx % 100 == 0:
                    print "datalist:",idx
                ofile.write("\n".join([" ".join(v) for v in data])+"\n")
                # for v in data:
                #     ofile.write()
                #     try:
                #         self.m_itemsets[v[0]][v[1]] += 1
                #     except:
                #         print "v:",v
                #         raise
                # for v in itertools.combinations(data,2):
                #     key0 = self.m_tranmap[v[0]]
                #     key1 = self.m_tranmap[v[1]]
                #     if key0 < key1:
                #         self.m_itemsets[str(key0)][str(key1)] += 1
                #     else:
                #         self.m_itemsets[str(key1)][str(key0)] += 1
        ofile.close()
        ifile.close()

        # if os.path.exists("fpgitemsetsrate"):
        #     os.remove("fpgitemsetsrate")
        # self.m_itemsetsrate = open("fpgitemsetsrate","c")
        # for idx in xrange(itemlen):
        #     self.m_itemsetsrate[str(idx)] = {}
        #     for idy in xrange(idx+1,itemlen):
        #         self.m_itemsetsrate[str(idx)][str(idy)] = self.m_itemsets * 1.0 / self.m_length
        # self.m_itemsets
        # self.m_itemsetsrate.close()

    def async(self,linelist):
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        pool = multiprocessing.Pool(40)
        signal.signal(signal.SIGINT, original_sigint_handler)
        try:
            # result = self.m_pool.map_async(self.mainfunc, doclist)
            result = pool.map_async(asyncfunc, zip([self.m_topo]*len(linelist),[self.m_tranmap]*len(linelist),linelist))
            result = result.get(99999999)  # Without the timeout this blocking call ignores all signals.
        except KeyboardInterrupt:
            pool.terminate()
            pool.close()
            pool.join()
            exit()
        else:
            pool.close()
        pool.join()
        return result

    def printfeq(self):
        fulldata = []
        for v in self.m_itemsetsrate:
            fulldata.extend(v)
        fulldata.sort()
        print "================================"
        print fulldata[-100:]

        fulldata = []
        for v in self.m_itemsets:
            fulldata.extend(v)
        fulldata.sort()
        print "================================"
        print fulldata[-100:]

        print self.m_length

    def save(self):
        jsontranmap = {}
        for key, value in self.m_tranmap.items():
            jsontranmap[str(key)] = value
        json.dump(jsontranmap,open("fpgtranmap","w"))
        # json.dump(self.m_itemsets,open("fpgitemsets","w"))
        # json.dump(self.m_itemsetsrate,open("fpgitemsetsrate","w"))
        json.dump(self.m_itemsetsroot,open("fpgitemsetsroot","w"))

    def load(self):
        jsontranmap = json.load(open("fpgtranmap"))
        self.m_tranmap = {}
        for key,value in jsontranmap.items():
            self.m_tranmap[DistinctWarning(warnstr=key)] = value
        # self.m_itemsets = shelve.open("fpgitemsets")
        self.m_itemsets = json.load(open("fpgitemsets"))
        # self.m_itemsetsrate = shelve.open("fpgitemsetsrate")
        if os.path.exists("fpgitemsetsroot"):
            self.m_itemsetsroot = json.load(open("fpgitemsetsroot"))

    def tongjicause(self, datadict, tjlen):
        self.m_itemsetsroot = []
        itemlen = len(self.m_tranmap)
        for idx in xrange(itemlen):
            self.m_itemsetsroot.append([])
            for idy in xrange(itemlen):
                self.m_itemsetsroot[-1].append({"key0root":0,"key1root":0})
        keylist = datadict.keys()
        keylist = keylist[:tjlen]
        idx = 0
        for curkey in keylist:
            alarmtimedict = datadict[curkey]
            idx += 1
            if idx % 10 == 0:
                print "fpgidx:",idx
            alarmlist = alarmtimedict.keys()
            for v in itertools.combinations(alarmlist,2):
                time0 = alarmtimedict[v[0]]
                time1 = alarmtimedict[v[1]]
                key0 = self.m_tranmap[v[0]]
                key1 = self.m_tranmap[v[1]]
                if key0 > key1:
                    tmp = key0
                    key1 = key0
                    key0 = tmp
                    tmp = time0
                    time1 = time0
                    time0 = tmp
                if time0 < time1:
                    self.m_itemsetsroot[key0][key1]["key0root"] += 1
                else:
                    self.m_itemsetsroot[key0][key1]["key1root"] += 1

    def printcauseinfo(self):
        itemlen = len(self.m_tranmap)
        alldata = []
        for idx in xrange(itemlen):
            for idy in xrange(itemlen):
                rootdata = self.m_itemsetsroot[idx][idy]
                key0root = rootdata["key0root"]
                key1root = rootdata["key1root"]
                totalkey = key0root + key1root
                if totalkey == 0:
                    continue
                else:
                    alldata.append(key0root * 1.0 / (totalkey))
        alldata.sort()
        doubledir = 0
        singledir = 0
        for v in alldata:
            if v == 1 or v == 0:
                singledir += 1
            else:
                doubledir += 1
        print singledir,doubledir

    def clusterdata(self, fname, ratethre = 0.2, secstep = 60):
        ifile = open(fname)
        notime = 0
        wrongcnt = 0
        datadict = {}
        doclen = 0
        print "start to read test file"
        for line in ifile:
            try:
                alarmcode,nename,happentime = line.strip().split("\t")
            except KeyboardInterrupt:
                raise
            except:
                notime += 1
                continue
            try:
                timesec = time.mktime( time.strptime(happentime,"%Y/%m/%d %H:%M:%S") )
            except:
                wrongcnt += 1
                continue
            doclen += 1
            if doclen % 1000 == 0:
                # print "read test file length:",doclen
                pass
            key = int(timesec) / secstep
            if key not in datadict:
                datadict[key] = {}
            warninfo = DistinctWarning(alarmcode,nename)
            if warninfo not in datadict[key] or datadict[key][warninfo] > timesec:
                datadict[key][warninfo] = timesec
        print "finish read test file"
        # 合并时间相近的告警
        print "start to combine slot"
        self.combineslot(datadict)
        print "finish combine slot"

        print "doclen:",doclen
        print "combinedlen:",sum([len(v) for v in datadict.values()])
        print "secstep:",secstep
        cmprate = sum([len(v) for v in datadict.values()]) * 1.0 / doclen
        print "compress rate:",cmprate

        # 合并同一时间段内位置相邻的告警
        print "start to combine in slot"
        rootcausedata = self.combinesinslot(datadict, ratethre)
        print "finish combine in slot"

        writerootcausedata = {}
        for key in rootcausedata:
            slotdata = rootcausedata[key]
            writekey = str(key)
            writerootcausedata[writekey] = dict([[v[0],str(v[1])] for v in slotdata.items()])
        json.dump(writerootcausedata,open("fpgrootcausedata","w"))

        print "doclen:",doclen
        print "combinedlen:",sum([len(v) for v in rootcausedata.values()])
        print "secstep:",secstep
        cmprate1 = sum([len(v) for v in rootcausedata.values()]) * 1.0 / doclen
        print "compress rate:",cmprate1
        print "diff:",cmprate - cmprate1

    # 合并时间槽内部的告警
    # 首先对同一时间槽内的不同告警分别编号，每有两个告警被合并就将其编号进行合并
    # 那么需要根据告警查到这个编号，然后再根据这个编号查到所有告警，那么需要两个辅助dict
    def combinesinslot(self,datadict,ratethre):
        rootcausedata = {}
        # idcount = 0
        print "datadict length:",len(datadict)
        datadictitems = datadict.items()
        keylist = [v[0] for v in datadictitems]
        dictlist = [v[1] for v in datadictitems]
        idx = 0
        for subdict in self.asynccombineinslot(dictlist,ratethre):
            key = keylist[idx]
            idx += 1
            rootcausedata[str(key)] = subdict
        return rootcausedata

    def asynccombineinslot(self,dictlist,ratethre):
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        pool = multiprocessing.Pool(40)
        signal.signal(signal.SIGINT, original_sigint_handler)
        try:
            # result = self.m_pool.map_async(self.mainfunc, doclist)
            dictlen = len(dictlist)
            para = zip([self.m_length]*dictlen,[self.m_itemsets]*dictlen,[ratethre]*dictlen,[self.m_topo]*dictlen,[self.m_tranmap]*dictlen,dictlist)
            result = pool.map_async(asynccombineinslotfunc, para)
            result = result.get(99999999)  # Without the timeout this blocking call ignores all signals.
        except KeyboardInterrupt:
            pool.terminate()
            pool.close()
            pool.join()
            exit()
        else:
            pool.close()
        pool.join()
        return result

    # 此方法会补足所有时间槽
    def combineslot(self,datadict):
        keylist = datadict.keys()
        keylist.sort()
        minslot = keylist[0]
        maxslot = keylist[1]
        keylist = range(minslot,maxslot +1)
        for idx in xrange(len(keylist) - 1,0,-1):
            combinedkey = keylist[idx]
            markkey = keylist[idx - 1]
            for warninfo in datadict.get(markkey,[]):
                if warninfo in datadict.get(combinedkey,[]):
                    del datadict[combinedkey][warninfo]

def asynccombineinslotfunc(para):
    length,itemsets,ratethre,topo,tranmap,slotwarndict = para
    rootcausedata = {}
    # slotwarndict = datadict[key]
    warnlist = slotwarndict.keys()
    warn2nodict = dict(zip(warnlist,range(len(warnlist))))
    no2warndict = dict(zip(range(len(warnlist)),[[v,] for v in warnlist]))
    # 合并位置相邻的告警
    # try:
    for v in itertools.combinations(warnlist,2):
        tranno1 = tranmap.get(v[0],None)
        tranno2 = tranmap.get(v[1],None)
        if tranno1 is None or tranno2 is None:
            continue
        if tranno2 < tranno1:
            temp = tranno2
            tranno2 = tranno1
            tranno1 = temp
        if TRAIN:
            itemsetkey = str(tranno1) + " " + str(tranno2)

            if itemsets.get(itemsetkey,0) * 1.0 / length < ratethre:
            # if self.m_itemsets[tranno1][tranno2] * 1.0 / self.m_length < ratethre:
                continue
        if topo.adjoin(v[0].m_nename,v[1].m_nename):
            warn1 = v[0]
            warn2 = v[1]
            no1 = warn2nodict[warn1]
            no2 = warn2nodict[warn2]
            if no1 == no2:
                continue
            for warn in no2warndict[no2]:
                warn2nodict[warn] = no1
            no2warndict[no1].extend(no2warndict[no2])
            del no2warndict[no2]
    # 根因确定，选择时间最前的
    for no in no2warndict:
        warnlist = no2warndict[no]
        oldesttime = slotwarndict[warnlist[0]]
        rootcause = warnlist[0]
        for warn in warnlist:
            if slotwarndict[warn] < oldesttime:
                oldesttime = slotwarndict[warn]
                rootcause = warn
        rootcausedata[str(no)] = rootcause
    # except:
    #     traceback.print_exc()
    #     print "warn2nodict:",warn2nodict
    #     print "no2warndict:",no2warndict
    #     raise
    return rootcausedata

def asyncfunc(para):
    topo,tranmap,line = para
    data = [DistinctWarning(warnstr=v) for v in line.strip().split("\t")]
    combinelist = []
    for v in itertools.combinations(data,2):
        key0 = tranmap.get(v[0],None)
        key1 = tranmap.get(v[1],None)
        if key0 is None or key1 is None:
            continue
        if not topo.adjoin(v[0].m_nename,v[1].m_nename):
            continue
        if key0 < key1:
            combinelist.append([str(key0),str(key1)])
        else:
            combinelist.append([str(key1),str(key0)])
    return combinelist

def genitemsets():
    ifile = open("../pairdata")
    itemsets = {}
    for line in ifile:
        key = line.strip()
        if key not in itemsets:
            itemsets[key] = 0
        itemsets[key] += 1
    ifile.close()
    length = 0
    ifile = open("../itemmining")
    for line in ifile:
        length += 1
    length *= 1.0
    for key in itemsets.keys():
        itemsets[key] /= length
    json.dump(itemsets,open("fpgitemsets","w"))

if __name__ == "__main__":
    pass
    # fpg = FPGrowth("../itemmining")
    # fpg.run()
    # fpg.save()
    # fpg.printfeq()

    fpg = FPGrowth("../itemmining")
    if TRAIN:
        fpg.run()
    else:
        fpg.load()
    for step in [v*30 for v in xrange(1,101)]:
        fpg.clusterdata("../testdata",secstep=step)

    # fpg = FPGrowth("../itemmining")
    # fpg.run()
    # fpg.save()
    # fpg.load()
    # print fpg.m_tranmap.keys()

    # a = [DistinctWarning("12","nename"), DistinctWarning("55","nename")]
    # print DistinctWarning("12","nename") in a
    # print "\t".join(a)

    # testdict = shelve.open("fpgitemsets")
    # testdict["6357"]

    # genitemsets()
    # itemsets = json.load(open("fpgitemsets"))
    # valuelist = itemsets.values()
    # valuelist.sort()
    # print valuelist[-1000:]