import re
class FileReader:
    def __init__(self, fname = None):
        self.m_file= None
        self.m_header = None
        self.m_headerlen = 0
        self.m_cachestr = ""
        self.m_cachedata = []

        if fname is not None:
            self.open(fname)

    def open(self,fname,openmode = "r"):
        self.m_file = open(fname,openmode)
        headerline = self.m_file.readline()
        headerdata= headerline.strip().split(",")
        self.m_header = [ v.strip('"') for v in headerdata]
        self.m_headerlen = len(self.m_header)
        self.m_cachestr = self.m_file.readline()
        self.m_cachestr = self.m_cachestr[1:]

    def getattridx(self,attr):
        return self.m_header.index(attr)

    def getattr(self,idx):
        return self.m_header[idx]

    def close(self):
        self.m_file.close()

    def getheader(self):
        self.m_file.readline()

    def _readtenline(self):
        lastline = ""
        for i in xrange(1000):
            lastline = self.m_file.readline()
            self.m_cachestr += lastline
        splitresult = re.split('","|"\r\n"',self.m_cachestr)
        if lastline == "":
            splitresult[-1] = splitresult[-1][:-1]
            self.m_cachedata.extend(splitresult)
            self.m_cachestr = ""
            return 0
        else:
            self.m_cachedata.extend(splitresult[:-1])
            self.m_cachestr = splitresult[-1]
            return 1

    def readtransection(self):
        while len(self.m_cachedata) < self.m_headerlen:
            if self._readtenline() == 0:
                break
        if len(self.m_cachedata) == self.m_headerlen:
            self.m_cachedata[-1] = self.m_cachedata[-1].strip('"\r')
        if len(self.m_cachedata) == 0 or len(self.m_cachedata) == 1:
            return None
        if len(self.m_cachedata) < self.m_headerlen:
            print "m_cachedata : ",self.m_cachedata
            print "m_cachestr : ",self.m_cachestr
            raise
        result = self.m_cachedata[:self.m_headerlen]
        self.m_cachedata = self.m_cachedata[self.m_headerlen:]
        return result

def testfilereader():
    # reader = FileReader("../1022.csv")
    # while True:
    #     print reader.readtransection()
    #     raw_input()
    # reader.close()

    reader = FileReader("../1023.csv")
    idx = 0
    while True:
        a = reader.readtransection()
        if a is None:
            break
        else:
            idx += 1
            # print idx
            # if idx == 399162:
            #     print a
            #     print reader.m_cachedata
            #     print reader.m_cachestr
    print "line count : ", idx
    reader.close()

if __name__ == "__main__":
    testfilereader()