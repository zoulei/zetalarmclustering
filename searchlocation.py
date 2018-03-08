from filereader import FileReader
from attributeparser import TopoInfo

def searchlocation(locstr):
    # filereader= FileReader("../NE_INFO.csv")
    # label = True
    topo = TopoInfo(full=True)
    ne = topo.getne(locstr)
    if ne is None:
        print "over"
    else:
        print "found:",locstr
        print "found NE:",str(ne)

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
    searchlocation("SU6095-SU2551")
    searchlocation("SU6095")
    searchlocation("LHDZ02_8G")
    searchlocation("LHDZ02")
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
    # searchlocation("435")
    # searchlocation("GBTSPANEL")
    # searchlocation("KS2603-K5775")
    # searchlocation("SM0233-SM1132")
    # searchlocation("SM0233_SM1132(LOW)")
    # searchlocation("Sm114-Sm2004")
    # searchlocation("SM0453-SM0220")
    # searchlocation("SM2403")
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
    # searchlocation("ZXMW_NR8120_899")
    # searchlocation("DZ1059-DZ1067")
    # searchlocation("DZ1059")
    # searchlocation("DZ1067")
    # searchlocation("BN:ME{131366167}")
    # searchlocation("SU2508")
    # searchlocation("SU1701")
    # searchlocation("SU2618")
    # searchlocation("SU6028")
    # searchlocation("SU2554")
    # searchlocation("SU6095")
    # searchlocation("SU2551")
    # calneidlen()
