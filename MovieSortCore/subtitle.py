from .filenameParser import FilenameParser

class Subtitle():

    formats = ['*/subs/*', '*/subtitles/*','*/sub/*', '*/subtitle/*']
    
    file                = FilenameParser()
    lang                = ''
    nameWithoutLanguage = ''
    
    def __init__(self):
        self.file                = FilenameParser()
        self.lang                = ''
        self.nameWithoutLanguage = ''

    def parse(self,  file, folder, movieName):
        self.file.parse(file, folder)
        pos = self.file.fileName.find(movieName)
        
        if pos == -1:
            return False
        
        pos = pos + len(movieName)
        self.lang                = self.file.fileName[pos+1:]
        self.nameWithoutLanguage = self.file.fileName[:pos]
        return True

    def serialize(self):
        j = dict()
        j['file']                = self.file.serialize()        
        j['lang']                = self.lang     
        j['nameWithoutLanguage'] = self.nameWithoutLanguage
        return j

    def deserialize(self, j: dict()):
        self.__init__()
        self.file.deserialize(j['file'])
        self.nameWithoutLanguage = j['nameWithoutLanguage']    
        self.lang                = j['lang']   