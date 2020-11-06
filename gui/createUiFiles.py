import os, subprocess

scriptpath = os.path.dirname(os.path.realpath(__file__))

def createUiFile(name : str):
    cmd = 'pyuic5 ' + scriptpath + \
            '/' + name + '.ui -o ' + scriptpath + '/Ui_' + name + '.py'
    subprocess.run(cmd)

createUiFile('MainWindow')
createUiFile('ShowSettings')
createUiFile('MovieSettings')
createUiFile('GeneralSettings')
createUiFile('CustomEnter')
createUiFile('MovieSelection')