#!/usr/bin/env python

__author__ = "Sascha Schiwy"
__copyright__ = "Copyright 2020, Sascha Schiwy"
__credits__ = []
__license__ = "GPLv2"
__version__ = "0.0.1"
__maintainer__ = "Sascha Schiwy"
__email__ = "sascha.schiwy@gmail.com"
__status__ = "Production"

import sys, getopt, json, os, fnmatch

from MovieSortCore import EpisodeMatcherTMDb, \
    getConfigParam, \
    TvShow, \
    Movie, \
    MovieMatcherTMDb, \
    getFileList, \
    Subtitle

from tmdbv3api import TMDb


def printHelp():
    print('MovieSortCmd -c <ConfigFile> [-d <DumpFile]')


def createShowDump(config: dict(), dumpFile: str):
    refetch = bool(getConfigParam(config, ["refetch_data"]))
    matcher = EpisodeMatcherTMDb(getConfigParam(config, ["tv_show_mode", "input_folder"]))
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
        matcher = parseShowFolder(config, matcher)

    # Fetch
    for show in matcher.tvShows.keys():
        if show.databaseId == -1:
            continue
        matcher.fetchDetails(show, show.databaseId)
    return matcher


def createMovieDump(config: dict(), dumpFile: str):
    refetch = bool(getConfigParam(config, ["refetch_data"]))
    matcher = MovieMatcherTMDb(getConfigParam(config, ["movie_mode", "input_folder"]))
    matcher.outputFormat = getConfigParam(config, ["movie_mode", "output_format"])

    if len(dumpFile) > 0:
        with open(dumpFile, "r") as readFile:
            data = json.load(readFile)
            for d in data:
                movie = Movie()
                movie.deserialize(d)
                matcher.movieData[movie] = None

        if not refetch:
            return matcher

    # No Dump given
    else:
        matcher = parseMovieFolder(config, matcher)

    # Fetch
    for movie in matcher.movieData.keys():
        matcher.fetchDetails(movie, movie.databaseId)
    return matcher


def parseShowFolder(config: dict, matcher: EpisodeMatcherTMDb):
    inDir = getConfigParam(config, ["tv_show_mode", "input_folder"])
    ignorePattern = getConfigParam(config, ["ignore_pattern"])
    files = getFileList(inDir, ignorePattern + Subtitle().formats)

    matcher.setFiles(files)
    possibleMatches = matcher.getDatabaseMatches()

    if bool(getConfigParam(config, ["set_auto_id"])):
        for r in possibleMatches:
            r[0].id = r[1][0].id
        return matcher

    for r in possibleMatches:
        print('For Show ' + r[0].estimatedTitle)
        for d in r[1]:
            if 'first_air_date' not in d.__dict__:
                continue

            print("ID: " + str(d.id) + \
                  '\tTitle: ' + d.name + \
                  " (" + str(d.first_air_date[:4]) + ")")

        id = -1

        print("Enter ID or nothing to accept first line, if available")
        i = input()
        if len(i) == 0 and len(r[1]) > 0:
            id = r[1][0].id
        elif len(i) > 0 and i.isdecimal:
            id = int(i)

        r[0].databaseId = id
    return matcher


def parseMovieFolder(config: dict(), matcher=MovieMatcherTMDb):
    inDir = getConfigParam(config, ["movie_mode", "input_folder"])
    ignorePattern = getConfigParam(config, ["ignore_pattern"])
    files = getFileList(inDir, ignorePattern + Subtitle().formats)

    matcher.rootFolder = inDir
    matcher.setFiles(files)

    possibleMatches = matcher.getDatabaseMatches()

    if bool(getConfigParam(config, ["set_auto_id"])):
        for r in possibleMatches:
            r[0].id = r[1][0].id
        return matcher

    for r in possibleMatches:
        print('For File: ' + r[0].file.fullNameAndPath)
        for d in r[1]:
            if 'release_date' not in d.__dict__.keys():
                continue

            print("ID: " + str(d.id) + \
                  '\tTitle: ' + d.title + \
                  " (" + str(d.release_date[:4]) + ")")
        id = -1
        print("Enter ID or nothing to accept first line, if available")
        i = input()
        if len(i) == 0 and len(r[1]) > 0:
            id = r[1][0].id
        elif len(i) > 0 and i.isdecimal:
            id = int(i)
        r[0].databaseId = id
    return matcher


def main(argv):
    configFile = ''
    dumpFile = ''

    try:
        opts, args = getopt.getopt(argv, "hc:d:", ["configfile=", "dumpfile"])
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

    if configFile == '':
        printHelp()
        sys.exit(0)

    config = dict()
    with open(configFile, "r") as readFile:
        config = json.load(readFile)

    TMDb().language = getConfigParam(config, ['language'])
    TMDb().api_key = 'e24fcd17eff0cfe0064fa7b5cb05b97d'

    overwrite = bool(getConfigParam(config, ["overwrite_files"]))

    showEnabled = bool(getConfigParam(config, ["tv_show_mode", "enable"]))
    movieEnabled = bool(getConfigParam(config, ["movie_mode", "enable"]))
    tmpFolder = getConfigParam(config, ["tmp_folder"])
    saveDump = bool(getConfigParam(config, ["dump_data"]))
    autoRename = bool(getConfigParam(config, ["auto_rename"]))

    showDump = None
    movieDump = None

    if showEnabled:
        showDump = createShowDump(config, dumpFile)
        showDump.determineRenaming()

    if movieEnabled:
        movieDump = createMovieDump(config, dumpFile)
        movieDump.determineRenaming()

    if saveDump and showDump != None:
        arr = []
        for show in showDump.tvShows.keys():
            arr.append(show.serialize())

        if not os.path.exists(tmpFolder):
            os.makedirs(tmpFolder)
        with open(tmpFolder + "/tv_shows.json", "w") as writeFile:
            json.dump(arr, writeFile, indent=4)

    if saveDump and movieDump != None:
        arr = []
        for movie in movieDump.movieData.keys():
            arr.append(movie.serialize())
        with open(tmpFolder + "/movies.json", "w") as writeFile:
            json.dump(arr, writeFile, indent=4)

    if autoRename and showDump != None:
        showDump.moveFiles(overwrite)
    if autoRename and movieDump != None:
        movieDump.moveFiles(overwrite)

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
