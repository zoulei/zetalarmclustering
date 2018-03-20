import itertools
import json
import copy

class FPGrowth:
    def __init__(self,fname=None):
        self.m_fname = fname
        self.initdocname()

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
                self.m_itemsets[key0][key1] += 1

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

    def load(self):
        self.m_tranmap = json.load(open("fpgtranmap"))
        self.m_itemsets = json.load(open("fpgitemsets"))
        self.m_itemsetsrate = json.load(open("fpgitemsetsrate"))

if __name__ == "__main__":
    fpg = FPGrowth("../itemmining")
    fpg.run()
    fpg.save()
    fpg.printfeq()

    # fpg = FPGrowth("../itemmining")
    # fpg.load()
    # fpg.printfeq()