from Constant import *
import re
import tongjisummary
from filereader import FileReader
import json

class NE:
    def __init__(self,ne_no,ne_name,ne_alias):
        self.m_no = ne_no
        self.m_name = ne_name
        # self.m_id = ne_id
        self.m_id = ne_alias

    def __eq__(self,other):
        if isinstance(other,str):
            return other in [self.m_no,self.m_name,self.m_id]
        elif isinstance(other, NE):
            return self.m_no == other.m_no and self.m_name == other.m_name and self.m_id == other.m_id

    def __hash__(self):
        return "|||".join([self.m_no , self.m_name , self.m_id])

    def __str__(self):
        return "|||".join([self.m_no , self.m_name , self.m_id])

    def __contains__(self, item):
        if item in self.m_name:
            return True
        return False

def testinfunction():
    a = NE("1","2345","32")
    print "23" in a

class TopoInfo:
    def __init__(self,full = True):
        if full:
            self.loadloc()
        else:
            self.loaddistinctloc()

    def loaddistinctloc(self):
        self.m_locdata = [NE(*v.split("|||")) for v in json.load(open("../distinctnedata"))]

    def loadloc(self):
        filereader= FileReader("../NE_INFO.csv")
        noidx = filereader.getattridx("NE_NO")
        nameidx = filereader.getattridx("NE_NAME")
        ididx = filereader.getattridx("ALIAS")
        self.m_locdata = []
        while True:
            tmptran = filereader.readtransection()
            if tmptran is None:
                break
            self.m_locdata.append(NE(tmptran[noidx],tmptran[nameidx],tmptran[ididx]))

    def testifylocname(self,name):
        return name in self.m_locdata

    def testifylocno(self,no):
        return no in self.m_locdata

    def getne(self,mark):
        for v in self.m_locdata:
            if mark == v:
                return v
        return None

    def getnebyname(self,name):
        targetne = self.getne(name)
        if targetne:
            return targetne
        for v in self.m_locdata:
            if name in v:
                return v
        return None

def testnenamereplicate():
    topo = TopoInfo(full=True)
    cnt = 0
    reduplicateidx = []
    for idx in xrange(len(topo.m_locdata)):
        for j in xrange(idx + 1,len(topo.m_locdata)):
            neone = topo.m_locdata[idx]
            netwo = topo.m_locdata[j]
            if neone == netwo:
                print idx,j,len(topo.m_locdata)
                print "ne one:",str(neone)
                print "ne two:",str(netwo)
                cnt += 1
                reduplicateidx.append(idx)
                break

    for idx in reduplicateidx[::-1]:
        del topo.m_locdata[idx]

    json.dump([str(v) for v in topo.m_locdata],open("../distinctnedata","w"))
    for idx in xrange(len(topo.m_locdata)):
        for j in xrange(idx + 1,len(topo.m_locdata)):
            neone = topo.m_locdata[idx]
            netwo = topo.m_locdata[j]
            # if neone == netwo:
            #     print idx,j,len(topo.m_locdata)
            #     print "error:",str(neone),str(netwo)
            #     cnt += 1
            #     reduplicateidx.append(idx)
            #     raise
            if neone.m_no == netwo:
                print idx,j,"------------"
                print "no",str(neone)
                print "no",str(netwo)
            # elif neone.m_name == netwo:
            #     print "name",str(neone),str(netwo)
            if neone.m_id == netwo:
                print idx,j,"------------"
                print "id",str(neone)
                print "id",str(netwo)
                raise
    print "cnt:",cnt

class Warning:
    def __init__(self, summary = None, location = None):
        self.m_summary = summary
        self.m_location = location
        self.m_pcdsummary = tongjisummary.summaryprocesser(self.m_summary).strip()
        self.m_type = self.identifysummarytp()

    def identifysummarytp(self):
        summary = self.m_summary
        pcdsummary = self.m_pcdsummary
        if len(pcdsummary) == 0:
            return TPERROR
        elif "BN:ME" in summary:
            return TP3
        elif "L eNBId" in summary:
            return TP4
        elif "alarmNeIp" in summary:
            return TP5
        elif "IpAddress" in summary:
            return TP7
        elif "EMS Server" in summary:
            return TP8
        elif "Alarm Content" in summary:
            return TP9
        elif "COMM:EMS" in summary:
            return TP11
        elif re.search("TIME.*vas_anyserv_module",summary):
            if pcdsummary.startswith("link"):
                return NOTP3
            else:
                return TP6
        elif pcdsummary.startswith("site"):
            return NOTP5
        elif pcdsummary.startswith("notification_id"):
            return NOTP4
        else:
            return TPDEFAULT

    def fetchsummarycontent(self):
        summary = self.m_summary
        cnt = ""
        if self.m_type in [TPERROR,NOTP4]:
            return None
        elif self.m_type == TP1:
            cnt = summary
        elif self.m_type == TP3:
            idx = summary.find("BN:ME")
            cnt = summary[:idx]
        elif self.m_type == TP4:
            idx = summary.find("L eNBId")
            cnt = summary[:idx]
        elif self.m_type == TP5:
            idx = summary.find("alarmNeIp")
            colonidx = summary.find(":")
            cnt = summary[colonidx:idx]
        elif self.m_type == TP6:
            idx = summary.find("TIME")
            cnt = summary[:idx]
        elif self.m_type == TP7:
            idx = summary.find("IpAddress")
            cnt = summary[:idx]
        elif self.m_type == TP8:
            cnt = "EMS Server"
        elif self.m_type == TP9:
            idx = summary.find("Alarm Content")
            semicolonidx = summary.find(";",idx)
            colonidx = summary.find(":")
            cnt = summary[:colonidx] + summary[idx + len("Alarm Content") : semicolonidx]
        elif self.m_type == TP11:
            idx = summary.find("COMM:EMS")
            cnt = summary[:idx]
        elif self.m_type == TPDEFAULT:
            searchresult = re.search(".*[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}",summary)
            if searchresult:
                prefixaddrstr = searchresult.group(0)
                cnt = summary[len(prefixaddrstr):]
            else:
                cnt = summary
        elif self.m_type == NOTP5:
            pass
        elif self.m_type == NOTP3:
            pass
        cnt = "".join(e for e in cnt if e.isalnum())
        cnt = cnt.lower()
        return cnt

    def fetchlocstr(self):
        location = self.m_location
        locname = None
        locno = None
        if self.m_type == TP3:
            idx = location.find("BN:ME{")
            endidx = location.find("}",idx)
            locno = location[idx :endidx+1]
        elif self.m_type == TP4:
            idx = location.find("NodeMe=")
            dotidx = location.find(",",idx)
            locno = location[idx+len("NodeMe="):dotidx]
        elif self.m_type == TP5:
            for idx, v in enumerate(location):
                if not v.isalnum() and v != " ":
                    locname = location[:idx]
                    break
        elif self.m_type == TP7:
            left = location.find("(")
            right = location.find(")")
            locname = location[left+1:right]
            if len(locname) == 0:
                result = re.search("IpAddress=[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}",location)
                if result:
                    locno = result.group(0)
                    locname = None
        elif self.m_type == TP8:
            pass
        elif self.m_type == TP11:
            pass
        elif self.m_type == NOTP4:
            pass
        elif self.m_type in [TP9, NOTP5]:
            idx = location.find("Site ID:")
            dotidx = location.find(",",idx)
            locno = location[idx+len("Site ID:"):dotidx]
        else:
            idx = location.find(",")
            if idx != -1:
                locname = location[:idx]

        if locname is not None:
            return locname
        elif locno is not None:
            return locno
        else:
            return None

    def fetchloc(self,topo):
        location = self.m_location
        locname = None
        locno = None
        if self.m_type == TP3:
            idx = location.find("BN:ME{")
            endidx = location.find("}",idx)
            locno = location[idx :endidx+1]
        elif self.m_type == TP4:
            idx = location.find("NodeMe=")
            dotidx = location.find(",",idx)
            if dotidx != -1:
                locno = location[idx+len("NodeMe="):dotidx]
            else:
                locno = location[idx+len("NodeMe="):]
        elif self.m_type == TP5:
            for idx, v in enumerate(location):
                if not v.isalnum() and v != " ":
                    locname = location[:idx]
                    break
        elif self.m_type == TP7:
            left = location.find("(")
            right = location.find(")")
            locname = location[left+1:right]
            if len(locname) == 0:
                result = re.search("IpAddress=[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}",location)
                if result:
                    locno = result.group(0)
                    locname = None
        elif self.m_type == TP8:
            pass
        elif self.m_type == TP11:
            pass
        elif self.m_type == NOTP4:
            pass
        elif self.m_type in [TP9, NOTP5]:
            idx = location.find("Site ID:")
            dotidx = location.find(",",idx)
            locno = location[idx+len("Site ID:"):dotidx]
            # print "locname:=================",locname,idx,dotidx
            # print location
        else:
            idx = location.find(",")
            if idx != -1:
                locname = location[:idx]

        if locname is not None:
            return topo.getnebyname(locname)
        elif locno is not None:
            return topo.getne(locno)
        else:
            return None

    def getfirstword(self):
        summary = self.m_pcdsummary
        firstspace = summary.find(" ")
        if firstspace == -1:
            target = summary
        else:
            target = summary[:firstspace]
        return target

class TestWarning:
    def __init__(self):
        self.m_topo = TopoInfo()

    def testfound(self):
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
                warn = Warning(summary,location)
                if warn.m_type == NOTP4:
                    continue
                ftword = warn.getfirstword()
                if ftword not in wholeresult:
                    wholeresult[ftword] = {"cnt":0,"good":0}
                wholeresult[ftword]["cnt"] += 1
                # content = warn.fetchsummarycontent()
                # if content is None:
                #     continue
                cnt += 1
                loc = warn.fetchloc(self.m_topo)
                if loc is None:
                    locstr = warn.fetchlocstr()
                    if locstr not in missloc:
                        missloc[locstr] = 0
                        print "==============================================="
                        print warn.m_summary
                        print "----------------------------------"
                        print warn.m_location
                        print "locstr:",warn.m_type,locstr
                    missloc[locstr] += 1
                    continue
                wholeresult[ftword]["good"] += 1
                found += 1
                # writefile.write(str(alarmcode)+"\t"+str(loc)+"\t"+tmptran[timeidx]+"\n")
        # writefile.close()

        print "result:"
        print "cnt:",cnt
        print "found:",found
        print "pcg:",found * 1.0 / cnt

        for v in wholeresult.keys():
            if wholeresult[v]["good"] == wholeresult[v]["cnt"]:
                del wholeresult[v]
            else:
                wholeresult[v]["pcg"] = wholeresult[v]["good"] * 1.0 / wholeresult[v]["cnt"]
        import pprint
        pprint.pprint(wholeresult)
        print "-----------------------"
        pprint.pprint(missloc)
        print "missloclen:",len(missloc)
        json.dump(wholeresult,open("tmpwholeresult","w"))
        json.dump(missloc,open("missloc","w"))

if __name__ == "__main__":
    TestWarning().testfound()
    # testnenamereplicate()
    # testinfunction()
    # TopoInfo().getnebyname("BH0040-BH0440  Sub S")