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

TRAIN = True

class DistinctWarning:
    def __init__(self, alarmcode = None, nename = None, content = None, warnstr = None):
        self.m_alarmcode = alarmcode
        self.m_nename = nename
        self.m_content = content
        if warnstr:
            self.loadfromstr(warnstr)

    def loadfromstr(self,warnstr):
        self.m_alarmcode,self.m_nename,self.m_content = warnstr.split("||||")

    def __str__(self):
        return self.m_alarmcode + "||||" + self.m_nename + "||||" + self.m_content

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
        ifile.close()

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
        self.genmap()

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

        ofile = open("../pairdata", "w")
        idy = 0
        # writedata = []
        for linelist in alllinelist:
            idy += 1
            # if idy == 2:
            #     break
            start = time.time()
            print "start async",start
            datalist = self.async(linelist)
            print "end async",time.time() - start
            idx = 0
            for data in datalist:
                idx += 1
                if idx % 100 == 0:
                    print "datalist:",idx
                if len(data) > 0:
                    ofile.write("\n".join([" ".join(v) for v in data])+"\n")
                # writedata.append("\n".join([" ".join(v) for v in data])+"\n")
        ofile.close()
        ifile.close()

        self.m_itemsets = genitemsets()
        self.genitemsetsrate()

    def genitemsetsrate(self):
        ifile = open(self.m_fname)
        fulldata = {}
        for line in ifile:
            nodata = line.strip().split("\t")
            for no in nodata:
                no = str(self.m_tranmap[DistinctWarning(warnstr=no)])
                if no not in fulldata:
                    fulldata[no] = 0
                fulldata[no] += 1
        self.m_itemsetsrate = {}
        for k,v in self.m_itemsets.items():
            try:
                no1,no2 = k.split(" ")
            except:
                print "k:",k
                raise
            negev = fulldata[no1] + fulldata[no2] - v * 2
            self.m_itemsetsrate[k] = v * 1.0 / (negev + v)

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
        fulldata = self.m_itemsetsrate.values()
        fulldata.sort()
        print "================================"
        print fulldata[-100:]
        print "--------------------------------"
        print fulldata[:100]

        fulldata = self.m_itemsets.values()
        fulldata.sort()
        print "================================"
        print fulldata[-100:]
        print "--------------------------------"
        print fulldata[:100]

        print self.m_length

    def save(self):
        jsontranmap = {}
        for key, value in self.m_tranmap.items():
            jsontranmap[str(key)] = value
        json.dump(jsontranmap,open("fpgtranmap","w"))
        # json.dump(self.m_itemsets,open("fpgitemsets","w"))
        json.dump(self.m_itemsetsrate,open("fpgitemsetsrate","w"))
        json.dump(self.m_itemsetsroot,open("fpgitemsetsroot","w"))

    def load(self):
        jsontranmap = json.load(open("fpgtranmap"))
        self.m_tranmap = {}
        for key,value in jsontranmap.items():
            self.m_tranmap[DistinctWarning(warnstr=key)] = value
        # self.m_itemsets = shelve.open("fpgitemsets")
        self.m_itemsets = json.load(open("fpgitemsets"))
        self.m_itemsetsrate = json.load(open("fpgitemsetsrate"))
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
        print singledir, doubledir

    def clusterdata(self, fname, ratethre = 0.2, secstep = 60):
        ifile = open(fname)
        notime = 0
        wrongcnt = 0
        datadict = {}
        doclen = 0
        print "start to read test file"
        for line in ifile:
            try:
                alarmcode,nename,summary,happentime = line.strip().split("\t")
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
            warninfo = DistinctWarning(alarmcode,nename,summary)
            if warninfo not in datadict[key] or datadict[key][warninfo] > timesec:
                datadict[key][warninfo] = timesec
        print "finish read test file"
        # 合并时间相近的告警
        # datadict 为二级dict，一级key为时间槽，二级key为warninfo，value为告警发生时间
        print "start to combine slot"
        self.combineslot(datadict)
        print "finish combine slot"

        print "doclen:",doclen
        print "combinedlen:",sum([len(v) for v in datadict.values()])
        print "secstep:",secstep
        cmprate = sum([len(v) for v in datadict.values()]) * 1.0 / doclen
        print "compress rate:",cmprate
        # raw_input("input")

        # 先屏蔽下面这些东西
        # 合并所属NE有共同父结点的告警
        # print "start to combine same father"
        # self.combinesamefather(datadict)
        # print "stop to combine same father"
        #
        # print "doclen:", doclen
        # combinedlen = 0
        # for fatherdictinfo in datadict.values():
        #     combinedlen += sum([len(v) for v in fatherdictinfo.values()])
        # print "combinedlen:", combinedlen
        # print "secstep:", secstep
        # cmprate3 = combinedlen * 1.0 / doclen
        # print "compress rate:", cmprate3

        # print "===========================same father data================================================"
        # for slot in datadict:
        #     print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        #     print "slot:",slot
        #     for father in datadict[slot]:
        #         print "**************************************************************************"
        #         print "father:", father
        #         print "================================================================"
        #         print "================================================================"
        #         print "================================================================"
        #         print "================================================================"
        #         for warn in datadict[slot][father]:
        #             print '-----------------------------------------------------------'
        #             print str(warn)

        # print "doclen:", doclen
        # print "combinedlen:", sum([len(v) for v in datadict.values()])
        # print "secstep:", secstep
        # cmprate3 = sum([len(v) for v in datadict.values()]) * 1.0 / doclen
        # print "compress rate:", cmprate3

        # 合并同一时间段内所属NE相同的告警，这是利用频繁项集挖掘
        # print "start to combine in ne"
        # self.combineinne(datadict,ratethre)
        # print "finish combine in ne"
        # print "threshold:",ratethre
        # print "combinedlen:",sum([len(v) for v in datadict.values()])
        # print "secstep:",secstep
        # cmprate2 = sum([len(v) for v in datadict.values()]) * 1.0 / doclen
        # print "compress rate:",cmprate2
        # print "diff:",cmprate - cmprate2
        #
        # # 合并同一时间段内位置相邻的告警
        # print "start to combine in slot"
        # # rootcausedata的内容为二级dict，第一层key为时间槽，第二层key为编号，第三层key为warn
        # rootcausedata = self.combinesinslot(datadict, ratethre)
        # print "finish combine in slot"
        #
        # writerootcausedata = {}
        # for key in rootcausedata:
        #     slotdata = rootcausedata[key]
        #     writekey = str(key)
        #     writerootcausedata[writekey] = dict([[v[0],str(v[1])] for v in slotdata.items()])
        # json.dump(writerootcausedata,open("fpgrootcausedata","w"))
        #
        # print "doclen:",doclen
        # print "combinedlen:",sum([len(v) for v in rootcausedata.values()])
        # print "secstep:",secstep
        # cmprate1 = sum([len(v) for v in rootcausedata.values()]) * 1.0 / doclen
        # print "compress rate:",cmprate1
        # print "diff:",cmprate2 - cmprate1
        # warnsamene = self.tongjineinfo(rootcausedata)
        # print "warsamene:", warnsamene * 1.0 / doclen
        # print "\n" * 5

        print "start to combine same father"
        datadict = self.combinesinslot(datadict, ratethre)
        print "stop to combine same father"

        print "doclen:", doclen
        combinedlen = 0
        for fatherdictinfo in datadict.values():
            combinedlen += len(fatherdictinfo)
        print "combinedlen:", combinedlen
        print "secstep:", secstep
        cmprate3 = combinedlen * 1.0 / doclen
        print "compress rate:", cmprate3

        # print "===========================combine data================================================"
        # for slot in datadict:
        #     print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        #     print "slot:",slot
        #     for father in datadict[slot]:
        #         print "**************************************************************************"
        #         print "father:", father
        #         print "================================================================"
        #         print "================================================================"
        #         print "================================================================"
        #         print "================================================================"
        #         for warn in datadict[slot][father]:
        #             print '-----------------------------------------------------------'
        #             print str(warn)

    def testclusteringresult(self):
        # 加载聚合结果数据
        rootcausedata = json.load(open("fpgrootcausedata"))

        for key in rootcausedata.keys():
            data = rootcausedata[key]
            for num in data.keys():
                data[num] = DistinctWarning(warnstr=data[num])
            neset = []
            for warn in data.values():
                if warn not in neset:
                    neset.append(warn)
            for nename in neset:
                for nename2 in neset:
                    if nename == nename2:
                        continue
                    if self.m_topo.adjoin(nename2.m_nename,nename.m_nename):
                        raise Exception
            print "========================================================"
            neset.sort(key=lambda v:v.m_alarmcode)
            print len(neset),len(data)
            for nename in neset:
                print str(nename)+",",

    def tongjineinfo(self, rootcausedata):
        warnsamene = 0
        for valuedict in rootcausedata.values():
            warninfolist = valuedict.values()
            neset = set()
            for warn in warninfolist:
                nename = warn.m_nename
                neset.add(nename)
            warnsamene += len(warninfolist) - len(neset)
        return warnsamene

    # 合并同一时间段内所属NE相同的告警
    def combineinne(self,datadict,ratethre):
        datadictitems = datadict.items()
        keylist = [v[0] for v in datadictitems]
        # dictlist 是每个slot中的warn与其发生时间的dict
        dictlist = [v[1] for v in datadictitems]
        idx = 0
        for subdict in self.asynccombineinne(dictlist,ratethre):
            key = keylist[idx]
            idx += 1
            datadict[key] = subdict

    # 合并同一时间段内所属NE相同的告警
    def combinesamefather(self, datadict):
        datadictitems = datadict.items()
        keylist = [v[0] for v in datadictitems]
        # dictlist 是每个slot中的warn与其发生时间的dict
        dictlist = [v[1] for v in datadictitems]
        idx = 0
        for subdict in self.asynccombinefather(dictlist):
            key = keylist[idx]
            idx += 1
            datadict[key] = subdict

    def asynccombineinne(self, dictlist,ratethre):
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        pool = multiprocessing.Pool(40)
        signal.signal(signal.SIGINT, original_sigint_handler)
        try:
            # result = self.m_pool.map_async(self.mainfunc, doclist)
            dictlen = len(dictlist)
            para = zip([self.m_length]*dictlen,[self.m_itemsetsrate]*dictlen,[ratethre]*dictlen,[self.m_topo]*dictlen,[self.m_tranmap]*dictlen,dictlist)
            result = pool.map_async(asynccombineinnefunc, para)
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

    def asynccombinefather(self,dictlist):
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        pool = multiprocessing.Pool(40)
        signal.signal(signal.SIGINT, original_sigint_handler)
        try:
            # result = self.m_pool.map_async(self.mainfunc, doclist)
            # dictlen = len(dictlist)
            # para = zip([self.m_length]*dictlen,[self.m_topo]*dictlen,[self.m_tranmap]*dictlen,dictlist)
            # result = pool.map_async(asynccombinefatherfunc, para)
            # result = result.get(99999999)  # Without the timeout this blocking call ignores all signals.
            result = []
            for dictdata in dictlist:
                result.append(asynccombinefatherfunc([self.m_length,self.m_topo,self.m_tranmap,dictdata]))
        except KeyboardInterrupt:
            pool.terminate()
            pool.close()
            pool.join()
            exit()
        else:
            pool.close()
        pool.join()
        return result

    # 合并时间槽内部的告警
    # 首先对同一时间槽内的不同告警分别编号，每有两个告警被合并就将其编号进行合并
    # 那么需要根据告警查到这个编号，然后再根据这个编号查到所有告警，那么需要两个辅助dict
    def combinesinslot(self,datadict,ratethre):
        rootcausedata = {}
        # idcount = 0
        print "datadict length:",len(datadict)
        # dictlist 是每个slot中的warn与其发生时间的dict
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
            # result = pool.map_async(asynctestfunc, para)
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

    def gethighestrate(self):
        return max(self.m_itemsetsrate.values())

def asynccombinefatherfunc(para):
    length,topo,tranmap,slotwarndict = para
    warnlist = slotwarndict.keys()
    # 先给所有的warn编个号，时间信息先不用
    # 合并位置相邻的告警
    fatherkeydata = {}
    for warn in warnlist:
        nename = warn.m_nename
        for father in topo.m_fatherdata.get(nename,[]):
            if father not in fatherkeydata:
                fatherkeydata[father] = []
            fatherkeydata[father].append(warn)
    # result = {}
    # for father in fatherkeydata.keys():
    #     lastwarn = fatherkeydata[father][0]
    #     for warn in fatherkeydata[father][1:]:
    #         if slotwarndict[warn] < slotwarndict[lastwarn]:
    #             lastwarn = warn
    #     result[lastwarn] = slotwarndict[lastwarn]
    # return result
    return fatherkeydata

def asynccombineinnefunc(para):
    length,itemsets,ratethre,topo,tranmap,slotwarndict = para
    # rootcausedata = {}
    # slotwarndict = datadict[key]
    newsubdict = {}
    warnlist = slotwarndict.keys()
    # 先给所有的warn编个号，时间信息先不用
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
            # 挖掘频繁项集，如果两个属于相同网元的告警频繁一起出现，那么就合并
            itemsetkey = str(tranno1) + " " + str(tranno2)
            if itemsets.get(itemsetkey,0) < ratethre:
            # if self.m_itemsets[tranno1][tranno2] * 1.0 / self.m_length < ratethre:
                continue
        # if topo.adjoin(v[0].m_nename,v[1].m_nename):
            warn1 = v[0]
            warn2 = v[1]
            no1 = warn2nodict[warn1]
            no2 = warn2nodict[warn2]
            if no1 == no2:
                continue
            # 把2号的数据合并到1号中
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
        # rootcausedata[str(no)] = rootcause
        newsubdict[rootcause] = slotwarndict[rootcause]
    return newsubdict
    # except:
    #     traceback.print_exc()
    #     print "warn2nodict:",warn2nodict
    #     print "no2warndict:",no2warndict
    #     raise
    # return rootcausedata

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

def asynctestfunc(para):
    length,itemsets,ratethre,topo,tranmap,slotwarndict = para
    rootcausedata = {}
    # slotwarndict = datadict[key]
    warnlist = slotwarndict.keys()
    warn2nodict = dict(zip(warnlist,range(len(warnlist))))
    no2warndict = dict(zip(range(len(warnlist)),[[v,] for v in warnlist]))
    # 合并位置相邻的告警
    # try:
    for v in itertools.combinations(warnlist,2):
        if topo.adjoin(v[0].m_nename,v[1].m_nename) or v[0].m_nename == v[1].m_nename:
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
    return no2warndict
    # 根因确定，选择时间最前的
    # for no in no2warndict:
    #     warnlist = no2warndict[no]
    #     oldesttime = slotwarndict[warnlist[0]]
    #     rootcause = warnlist[0]
    #     for warn in warnlist:
    #         if slotwarndict[warn] < oldesttime:
    #             oldesttime = slotwarndict[warn]
    #             rootcause = warn
    #     rootcausedata[str(no)] = rootcause
    # # except:
    # #     traceback.print_exc()
    # #     print "warn2nodict:",warn2nodict
    # #     print "no2warndict:",no2warndict
    # #     raise
    # return rootcausedata

def asyncfunc(para):
    topo,tranmap,line = para
    data = [DistinctWarning(warnstr=v) for v in line.strip().split("\t")]
    combinelist = []
    for v in itertools.combinations(data,2):
        key0 = tranmap.get(v[0],None)
        key1 = tranmap.get(v[1],None)
        if key0 is None or key1 is None:
            continue
        if v[0].m_nename != v[1].m_nename:
            continue
        # if not topo.adjoin(v[0].m_nename,v[1].m_nename):
        #     continue
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
    json.dump(itemsets,open("fpgitemsets","w"))
    return itemsets

if __name__ == "__main__":
    # fpg = FPGrowth("../itemmining")
    # fpg.testclusteringresult()
    # fpg.run()
    # fpg.m_itemsets = json.load(open("fpgitemsets"))
    # fpg.genitemsetsrate()

    # raise
    #
    # pass
    fpg = FPGrowth("../itemmining")
    fpg.run()
    fpg.save()
    hr = fpg.gethighestrate()
    fpg.clusterdata("../testdata",0.000000000001)


