
# FileSort
Still under deployment, neither the software nor the documentation is finished yet.

## Summary
FileSort is a tool to automatically move video and tv-show files. Therefore, it uses [The Movie Database](https://www.themoviedb.org/) to fetch the movie data online. The software is written in Python.

## Features
- Parse filenames in a defined folder and subfolders
- Obtain information from TMDb about parsed files
- Accept the tools pruposal or enter the show ID by your own
- Create dumps of matched data and give the possibilty to customize the output
- Move the matched files
- Custom renaming pattern
- Ignore specified pattern in filenames like, e.g. *.nfo

And more...


## Missing Features
- Movie Mode is not implemented yet
- GUI not started
- Document the code
- Cleanup the code

## Reason for the Project
I wanted to learn python, since I like to have a usage of a project I decided to create a software to rename file in an automatized way. I like the capabilities of [FileBot](https://www.filebot.net/), and decided to create something like a clone. However, I want to keep the sources and usage free for anyone and licenced it under GPL.

## Graphical User Interface
T.B.D 

### Output format
|Symbol| Replacement                               |
|------|-------------------------------------------|
|%n    | Show Name                                 |
|%s    | Season Number                             |
|%0s   | Season Number, Zero Padded [01, 02...]    |
|%00s  | Season Number, Zero Padded [001, 002...]  |
|%e    | Episode Number                            |
|%0e   | Episode Number, Zero Padded [01, 02...]   |
|%00e  | Episode Number, Zero Padded [001, 002...] |
|%t    | Episode Title                             |
|%y    | First Air Year                            |
|%x    | File Extension                            |

 ## Command Line Tool
 Beside the GUI the project contains a command line tool version of FilesSort. It can be used on a headless system like a download server or to automatize tasks.

The command line tool uses a .json file to be configured. An example is shown below.

~~~~{.json} 
{
    "tv_show_mode":{
        "output_format" : "./%n (%y)/Season %0s/%n (%y) - S%0sE%0e - %t.%x",
        "input_folder" : "./",
        "enable": true
    },
    "movie_mode":{
        "output_format" : "%t (%y)/%t (%y).%x",
        "input_folder" : "./",
        "enable": false
    },
    "language" : "en",
    "dump_data" : true, 
    "dump_renaming_list" : true,
    "auto_rename" : false,
    "set_auto_id": false,
    "tmp_folder" : "./tmp/",
    "refetch_data" : false,
    "overwrite_existing" : false,
    "ignore_pattern": ["*.nfo", "*.jpg", "*.htm", "*.html", '*.txt', "*.png", "*sample*"]
}
~~~~

## Development Requirements
https://pypi.org/project/tmdbv3api/
~~~~
pip install tmdbv3api
~~~~

## Contributions
Feel free to send pull requests, use git-flow-workflow.

## Credits
[Anthony Bloomer](https://github.com/AnthonyBloomer)
[The Movie Database](https://www.themoviedb.org/)