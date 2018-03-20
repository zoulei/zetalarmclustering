import itertools
import os

def tran2pair():
    ifile = open("../itemmining")
    ofile = open("../tmp","w")
    for line in ifile:
        data = line.strip().split(" ")
        for v in itertools.combinations(data, 2):
            ofile.write(" ".join(v)+"\n")
    ifile.close()
    ofile.close()
    os.system("mv ../tmp ../itemmining")

if __name__ == "__main__":
    tran2pair()
