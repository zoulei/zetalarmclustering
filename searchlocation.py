from filereader import FileReader
from attributeparser import TopoInfo

def searchlocation(locstr):
    # filereader= FileReader("../NE_INFO.csv")
    # label = True
    topo = TopoInfo()
    ne = topo.getne(locstr)
    if ne is None:
        print "over"
    else:
        print "found:",locstr

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
    # searchlocation("DZ1067-LHDZ02_8G")
    # searchlocation("DZ1062-DZ2406")
    # searchlocation("SU6029-SU6037")
    # searchlocation("56008")
    # searchlocation("BN:ME{131366445}")
    # searchlocation("SM2607_S1")
    # searchlocation("DZ0395-DZ1070")
    # searchlocation("SM2607_s1")
    # searchlocation("BHZMS15")
    # searchlocation("Namangan")
    # searchlocation("Namangan HLR")
    # searchlocation("Namangan HLR-USPP_3")
    # searchlocation("DNZMG1")
    # searchlocation("Samarkand")
    # searchlocation("Samarkand HLR")
    # searchlocation("SM1121-SM0118")
    # searchlocation("VMS")
    # searchlocation("BH1039-BH2611")
    # searchlocation("BHBN01-BH1603 Main")
    # searchlocation("BH1610-BH1072 NEW")
    # searchlocation("EMS Server")
    # searchlocation("EMS")
    # searchlocation("BH0435-G_VIP_S0")
    # searchlocation("BH0435")
    searchlocation("435")
    # searchlocation("GBTSPANEL")
    # searchlocation("KS2603-K5775")
    # searchlocation("SM0233-SM1132")
    # searchlocation("SM0233_SM1132(LOW)")
    # searchlocation("Sm114-Sm2004")
    # searchlocation("SM0453-SM0220")
    searchlocation("SM2403")
    # searchlocation("1939581319462")
    # searchlocation("ZXMW PR10")
    # searchlocation("ZXMW")
    # searchlocation("ZXMW_NR8120_900")
    # searchlocation("ZXMW_NR8120")
    # searchlocation("Sigtran")
    # searchlocation("MGW")
    # searchlocation("Bukhara MGW-NGMGW_W_35")
    # searchlocation("Bukhara")
    # searchlocation("MGW-NGMGW_W_35")
    # searchlocation("i2pn5pmd-8")
    # searchlocation("Bukhara ZTE CG")
    # searchlocation("Bukhara MGW")
    # searchlocation("SC")
    # searchlocation("SM2607_S1")
    # searchlocation("SM2614_S2")
    # searchlocation("SM5607")
    # searchlocation("NV1023-G_HUB(10)_S0")
    # searchlocation("92")
    # searchlocation("1023")
    # searchlocation("BH0435-G_VIP_S0")
    searchlocation("ZXMW_NR8120_899")
    # calneidlen()
