#! /usr/bin/env python3

class FileHelper(object):
    def __init__(self):
        self.filedir = None
        self.splitedfile = {}

    def setfile(self,filedir): 
        self.filedir = filedir

    def writetofile(self, data):
        f = open(self.filedir, "a+")
        f.write(data)
        f.close()

    def reset(self):
        self.filedir = None
        self.splitedfile = {}

