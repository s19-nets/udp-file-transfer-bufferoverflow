#! /usr/bin/env python3

class FileHelper(object): 
    def __init__(self): 
        self.filedir = None
        self.splitedfile = {}

    def setfile(self,filedir): 
        self.filedir = filedir

    def splitfile(self): 
        f = open(self.filedir, "rb")
        i = 1
        data = f.read(100)
        while data: 
            self.splitedfile[i] = data
            data = f.read(100)
            i += 1
        f.close()

    def getsegment(self, segnum): 
        return self.splitedfile[segnum] if segnum in self.splitedfile else -1

    def fileexists(self, filedir): 
        return os.path.isfile(filedir)

    def writetofile(self, data): 
        f = open(self.filedir, "a")
        f.write(data)
        f.close()

    def reset(self): 
        self.filedir = None
        self.splitedfile = {}

