from typing import List
import os
from pathlib import Path
import re
import json

from Globals import Globals

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

class Dateien:


    ###----------EEG:----------###


    @staticmethod
    def get_fileList(pathFolder : Path) -> List[str]:
        
        dirList : List[str] = os.listdir(pathFolder)
        fileList : List[str] = []

        for entry in dirList:
            if os.path.isfile(pathFolder / entry) == True:
                fileList.append(entry)
        return fileList
    



    @staticmethod
    def get_properFileList(searchPattern : str, pathFolder : Path) -> List[str]:

        fileList : List[str] = Dateien.get_fileList(pathFolder)
        properFileList : List[str] = []
        
        for fileName in fileList:
            if( re.search(searchPattern, fileName) != None):
                properFileList.append(fileName)
        return properFileList
    



def test_searchDatei():
    participantNr : int = 77
    #print( Globals.get_searchPatternDict(participantNr).keys() ) # shows all available search patterns

    globals : object = Globals(mode="testMode")
    searchPath : Path = Globals.get_pathBVR_rohDatenFolder(globals.mode)
    searchPatternDict = Globals.get_searchPatternDict(participantNr)
    searchPattern = searchPatternDict["SEARCH_PATTERN_eeg_additionalFiles"]

    y = Dateien.get_fileList(searchPath)
    print(y)
    x = Dateien.get_properFileList(searchPattern, searchPath)
    print(x)






