#!/usr/bin/env python

__author__     = "Sascha Schiwy"
__copyright__  = "Copyright 2020, Sascha Schiwy"
__credits__    = ["Anthony Bloomer", "The Movie Database"]
__license__    = "GPLv2"
__version__    = "0.0.1"
__maintainer__ = "Sascha Schiwy"
__email__      = "sascha.schiwy@gmail.com"
__status__     = "Production"

import sys, getopt, json, os, shutil, fnmatch

from core.cmdConfig import CmdConfig
from core.episodeMatcher import EpisodeMatcherTMDb, TvShow

def printHelp():
    print('FileSortCmd -c <ConfigFile> [-d <DumpFile]')
    print('FileSortCmd -c <ConfigFile> -r <RenameFile>')

def moveFiles(files : [], overwrite : bool):
    for source, target in files:
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
            print ('move ' + source + ' target' + target)
            shutil.move(source, target)

def getConfigParam(config : dict(), keys : []):
    param  = config
    failed = False
    
    for key in keys:
        if key in param:
            param = param[key]
            continue
        else:
            failed = True
            break

    if failed:
        param = CmdConfig
        for key in keys:
            param = param[key]

        print(["WARN: Could not read parameter for keys: ", keys, " use default: ", param])
    return param

def createShowDump(config : dict(), dumpFile : str):
    
    refetch = bool(getConfigParam(config, ["refetch_data"]))
    matcher = EpisodeMatcherTMDb()
    matcher.setLanguage(getConfigParam(config, ["language"]))
    matcher.outputFormat = getConfigParam(config, ["tv_show_mode", "output_format"])
    
    if len(dumpFile) > 0:
        with open(dumpFile, "r") as readFile:
            data = json.load(readFile)
            for d in data:
                show = TvShow()
                show.deserialize(d)
                matcher.tvShows[show] = None
        
        if not refetch:
            return matcher
    
    else:
        matcher = parseFolder(config, matcher)
    
    # Fetch
    for show in matcher.tvShows.keys():
        matcher.fetchDetails(show, show.id)
    return matcher

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
                fileList.append(f)
    
    return fileList

def parseFolder(config : dict, matcher : EpisodeMatcherTMDb):
    inDir         = getConfigParam(config, ["tv_show_mode", "input_folder"])
    ignorePattern = getConfigParam(config, ["ignore_pattern"])
    files         = getFileList(inDir, ignorePattern)   
    
    matcher.setFiles(files)
    result = matcher.getDatabaseMatches()

    if bool(getConfigParam(config, ["set_auto_id"])):
        for r in result:
            r[0].id = r[1][0].id
        return matcher
    
    for r in result:
        for d in r[1]:
            print("ID: " + str(d.id) + \
                '\tTitle: ' + d.obj_name + \
                    " (" + str(d.first_air_date[:4]) + ")")
        
        id = -1
        while id == -1:
            print("Enter ID or nothing to acceppt first line, if available")
            i = input()
            if len(i) == 0 and len(r[1]) > 0:
                id = r[1][0].id
            elif i.isdecimal:
                id = int(i)
        
        r[0].id = id
    return matcher

def main(argv):

    configFile   = ''
    renameFile   = ''
    dumpFile   = ''

    try:
        opts, args = getopt.getopt(argv,"hc:r:d:",["configfile=", "renamefile", "dumpfile"])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit(0)
        elif opt in ("-c", "--configfile"):
            configFile = arg
        elif opt in ("-d", "--dumpfile"):
            dumpFile = arg
        elif opt in ("-r", "--renamefile"):
            renameFile = arg

    if configFile == '' and renameFile == '':
        printHelp()
        sys.exit(0)

    config = dict()
    with open(configFile, "r") as readFile:
            config = json.load(readFile)

    overwrite = bool(getConfigParam(config, ["overwrite_existing"]))

    if len(renameFile) > 0:
        with open(renameFile, "r") as readFile:
            data = json.load(readFile)
            moveFiles(data, overwrite)
            sys.exit(0)
    
    showEnabled = bool(getConfigParam(config, ["tv_show_mode" , "enable"]))
    tmpFolder   = getConfigParam(config, ["tmp_folder"])
    saveDump    = bool(getConfigParam(config, ["dump_data"]))
    saveRen     = bool(getConfigParam(config, ["dump_renaming_list"]))
    autoRename  = bool(getConfigParam(config, ["auto_rename"]))

    showDump   = None
    if showEnabled:
        showDump   = createShowDump(config, dumpFile)
        showDump.determineRenaming()


    if saveDump and showDump != None:
        arr = []
        for show in showDump.tvShows.keys():
            arr.append(show.serialize())
        with open(tmpFolder + "/tv_shows.json", "w") as writeFile:
            json.dump(arr, writeFile, indent=4)  

    if saveRen:
        with open(tmpFolder + "/tv_shows_rename.json", "w") as writeFile:
            json.dump(showDump.matchedFiles, writeFile, indent=4)    

    if autoRename:
        moveFiles(showDump.matchedFiles, overwrite)

    sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])

