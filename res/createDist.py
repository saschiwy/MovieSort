import os, subprocess

scriptpath  = os.path.dirname(os.path.realpath(__file__))
pyinstaller = 'C:/Users/Sascha/AppData/Local/Programs/Python/Python37/Scripts/pyinstaller.exe'

cmd = pyinstaller + ' --clean --add-binary ' + scriptpath + '/qtmodern*' + os.pathsep + 'qtmodern ' \
    + '--distpath ' + scriptpath + '/dist ' \
    + '--workpath ' + scriptpath + '/build ' \
    + '--noconsole --onefile -y ' \
    + scriptpath + '/../MovieSort.py'
subprocess.run(cmd)

cmd = pyinstaller + ' --clean --onefile -y ' \
    + '--distpath ' + scriptpath + '/dist ' \
    + '--workpath ' + scriptpath + '/build ' \
    + scriptpath + '/../MovieSortCmd.py'
subprocess.run(cmd)
