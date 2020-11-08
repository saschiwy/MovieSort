import datetime
from os import path

from .filenameParser import FilenameParser
from .fops import getFileList, moveFile
from .subtitle import Subtitle

class Movie():
    
    file                = None
    estimatedTitle      = None
    estimatedTitleFrags = None
    databaseTitle       = None
    databaseId          = None
    databaseYear        = None
    estimatedYear       = None
    subs                = None

    def __init__(self):
        self.file                = FilenameParser()
        self.estimatedTitle      = ''
        self.estimatedTitleFrags = []
        self.databaseTitle       = ''
        self.databaseYear        = 1900
        self.databaseId          = -1
        self.estimatedYear       = 1900
        self.subs                = []
    
    def __isYear__(self, string : str):
        if not string.isdecimal():
            return [False, 0]
        
        y = int(string)
        if y > 1900 and y <= datetime.datetime.now().year:
            return [True, y]
        
        return [False, 0]

    def parse(self, name : str, rootFolder):
        self.file.parse(name, rootFolder)

        for s in self.file.parsedNames:
            result = self.__isYear__(s)
            
            if result[0]:
                self.estimatedYear = result[1]
                break
            
        for s in self.file.parsedNames:
            if s.lower() in self.file.cutter:
                break
            self.estimatedTitleFrags.append(s)
            
        self.estimatedTitle      = ' '.join(self.estimatedTitleFrags)

        # Check for subtitles
        subsPath = self.file.filepath + '/subs'
        if path.exists(subsPath) and path.isdir(subsPath):
            self.getSubtitles(subsPath)

        subsPath = self.file.filepath + '/subtitles'
        if path.exists(subsPath) and path.isdir(subsPath):
            self.getSubtitles(subsPath)

    def getSubtitles(self, path):
        files = getFileList(path, [])
        for file in files:
            sub = Subtitle()
            if sub.parse(file, path, self.file.fileName):
                self.subs.append(sub)
    
    def setTarget(self, target : str):
        target = target.replace("\\", "/")
        self.file.targetFileName = target

        if len(self.subs) == 0:
            return
        pos        = target.rfind("/") + 1
        subsFolder = target[:pos] + 'Subs/'
        filename   = target[pos:target.rfind('.')]

        for sub in self.subs:
            sub.file.targetFileName = subsFolder + filename + '-' + sub.lang + '.' + sub.file.extension
    
    def move(self, overwrite):
        if self.file.targetFileName == '':
            return
        
        moveFile(self.file.fullNameAndPath, self.file.targetFileName, overwrite)
        for sub in self.subs:
            moveFile(sub.file.fullNameAndPath, sub.file.targetFileName, overwrite)

    def serialize(self):
        j = dict()
        j['file']                = self.file.serialize()        
        j['estimatedTitle']      = self.estimatedTitle     
        j['estimatedTitleFrags'] = self.estimatedTitleFrags
        j['databaseTitle']       = self.databaseTitle      
        j['databaseYear']        = self.databaseYear      
        j['databaseId']          = self.databaseId
        j['estimatedYear']       = self.estimatedYear
        
        subs = []
        for sub in self.subs:
            subs.append(sub.serialize())
        j['subs']                = subs

        return j

    def deserialize(self, j: dict()):
        self.__init__()
        self.file                = FilenameParser()
        self.file.deserialize(j['file'])
        self.estimatedTitle      = j['estimatedTitle']     
        self.estimatedTitleFrags = j['estimatedTitleFrags']
        self.databaseTitle       = j['databaseTitle']    
        self.estimatedYear       = j['estimatedYear']    
        self.databaseYear        = j['databaseYear']    
        self.databaseId          = j['databaseId']   
        for sub in j['subs']:
            self.subs.append(Subtitle().deserialize(sub))