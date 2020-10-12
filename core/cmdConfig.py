CmdConfig = {
    "tv_show_mode":{
        "output_format" : "./%n (%y)/Season %0s/%n (%y) - S%0sE%0e - %t.%x",
        "input_folder" : "./",
        "enable": True
    },

    "movie_mode":{
        "output_format" : "%t (%y)/%t (%y).%x",
        "input_folder" : "./",
        "enable": False
    },

    "language" : "en",
    "dump_data" : True, 
    "dump_renaming_list" : True,
    "auto_rename" : True,
    "set_auto_id": False,
    "tmp_folder" : "./tmp/",
    "refetch_data" : False,
    "overwrite_files" : False,
    "ignore_pattern": ["*.nfo", "*.jpg", "*.htm", "*.html", "*.url", '*.txt', "*.png", "*sample*", "*proof*", ".DS_Store"]
}

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