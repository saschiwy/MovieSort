import os, fnmatch, sys, shutil, string, unicodedata

def moveFile(source : str, target : str, overwrite : bool):
    pos       = target.rfind("/")
    targetDir = "./"
    if pos != -1:
        targetDir = target[:pos]
    # check if directory exists or not yet
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)

    if os.path.isfile(target) and overwrite:
        os.remove(target)

    if os.path.exists(targetDir):
        try:
            shutil.move(source, target)
        except : None

def isFileToBeAddToList(file, ignorePattern):
    for x in ignorePattern:
        if fnmatch.fnmatch(file, x):
            return False
    return True

def getFileList(path, ignorePattern):
    fileList = []

    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            if isFileToBeAddToList(f, ignorePattern):
                fileList.append(f.replace('\\', '/'))
    
    return fileList

validFilenameChars = ":-_.()/ %s%s" % (string.ascii_letters, string.digits)

def removeAllExceptFirst(s : str,substr : str):
    try:
        first_occurrence = s.index(substr) + len(substr)
    except ValueError:
        pass
    else:
        s = s[:first_occurrence] + s[first_occurrence:].replace(substr, "")
    return s

def removeDisallowedFilenameChars(filename):
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('utf-8')
    cleanedFilename = ''.join(c for c in cleanedFilename if c in validFilenameChars)
    return removeAllExceptFirst(cleanedFilename, ":")