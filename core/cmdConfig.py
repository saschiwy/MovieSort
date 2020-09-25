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
    "auto_rename" : False,
    "set_auto_id": False,
    "tmp_folder" : "./tmp/",
    "refetch_data" : False,
    "overwrite_existing" : False,
    "ignore_pattern": ["*.nfo", "*.jpg", "*.htm", "*.html", '*.txt', "*.png", "*sample*"]
}