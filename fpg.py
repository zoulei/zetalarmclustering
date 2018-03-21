import itertools
import json
import copy
import os

class FPGrowth:
    def __init__(self,fname=None):
        self.m_fname = fname
        self.initdocname()
        self.m_itemsetsroot = {}

    def initdocname(self):
        self.m_length = 0
        ifile = open(self.m_fname)
        for line in ifile:
            self.m_length += 1

    def genreversemap(self):
        self.m_reversemap = {}
        for key,value in self.m_tranmap.items():
            self.m_reversemap[value] = key

    def genmap(self):
        self.m_tranmap = {}
        transet = set()
        ifile = open(self.m_fname)
        idx = 0
        for line in ifile:
            idx += 1
            if idx % 1000 == 0:
                print idx
            data = line.strip().split(" ")
            for v in data:
                transet.add(v)
        for idx,v in enumerate(list(transet)):
            self.m_tranmap[v] = idx
        ifile.close()
        self.genreversemap()

    def run(self):
        self.genmap()
        itemlen = len(self.m_tranmap)
        self.m_itemsets = []
        for idx in xrange(itemlen):
            self.m_itemsets.append([0]*itemlen)
        ifile = open(self.m_fname)
        idx = 0
        for line in ifile:
            idx += 1
            if idx % 1000 == 0:
                print idx
            data = line.strip().split(" ")
            for v in itertools.combinations(data,2):
                key0 = self.m_tranmap[v[0]]
                key1 = self.m_tranmap[v[1]]
                if key0 < key1:
                    self.m_itemsets[key0][key1] += 1
                else:
                    self.m_itemsets[key1][key0] += 1

        self.m_itemsetsrate = copy.deepcopy(self.m_itemsets)
        for idx in xrange(itemlen):
            for idy in xrange(itemlen):
                self.m_itemsetsrate[idx][idy] /= self.m_length * 1.0

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
        json.dump(self.m_tranmap,open("fpgtranmap","w"))
        json.dump(self.m_itemsets,open("fpgitemsets","w"))
        json.dump(self.m_itemsetsrate,open("fpgitemsetsrate","w"))
        json.dump(self.m_itemsetsroot,open("fpgitemsetsroot","w"))

    def load(self):
        self.m_tranmap = json.load(open("fpgtranmap"))
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
        print singledir,doubledir

if __name__ == "__main__":
    # fpg = FPGrowth("../itemmining")
    # fpg.run()
    # fpg.save()
    # fpg.printfeq()

    # fpg = FPGrowth("../itemmining")
    # fpg.load()
    # fpg.printcauseinfo()

    fpg = FPGrowth("../itemmining")
    fpg.run()
    fpg.save()
    fpg.load()
    print fpg.m_tranmap.keys()