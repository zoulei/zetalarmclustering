import sys

def readprocesstime():
    fname = sys.argv[1]
    datas = []
    ifile = open(fname)
    for line in ifile:
        for starts in ["secstep:","compress rate:","diff:","warsamene:"]:
            if line.startswith(starts):
                datastr = line.strip().split(" ")[-1]
                datas.append(datastr)
                break

    grouplen = 6
    ofile = open("fpgclean","w")
    ofile.write("\t".join(["SECSTEP","CMPRATE","INSLOTCMPRATE","DIFF","WARSAME"])+"\n")
    for idx in xrange(len(datas) / 6):
        realidx = idx * 6
        secstep = datas[realidx]
        cmprate = datas[realidx + 1]
        inslotcmprate = datas[realidx + 3]
        diff = datas[realidx + 4]
        warsame = datas[realidx + 5]
        ofile.write("\t".join([secstep,cmprate,inslotcmprate,diff,warsame])+"\n")

if __name__ == "__main__":
    readprocesstime()