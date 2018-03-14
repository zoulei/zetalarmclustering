# -*- coding:utf-8 -*-
import time

def generateitemsetminingrawdata(secstep=60):
    ifile = open("../cleandata")
    datadict = {}
    for line in ifile:
        alarmcode,nename,happentime = line.strip().split("\t")
        timesec = time.strptime(happentime,"%Y/%m/%d %H:%M:%S")
        key = int(timesec) / secstep
        if key not in datadict:
            datadict[key] = []
        datadict[key].append(alarmcode)
    ifile.close()

    ofile = open("../itemmining","w")
    for key in datadict:
        ofile.write(" ".join(datadict[key])+"\n" )
    ofile.close()

if __name__ == "__main__":
    generateitemsetminingrawdata()