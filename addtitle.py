import os

def addtitleforfile(fname,titlefname):
    title = open(titlefname).readline()
    tempfile = open("tempfilefortitle","w")
    tempfile.write(title)
    ofile = open(fname)
    for line in ofile:
        tempfile.write(line)
    tempfile.close()
    ofile.close()
    os.system("mv "+fname+" "+fname+"_backup")
    os.system("mv "+"tempfilefortitle"+" "+fname)

if __name__ == "__main__":
    addtitleforfile("../1125.csv","../1126.csv")