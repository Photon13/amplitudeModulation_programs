from Paths import Paths

from typing import List
from pathlib import Path
import os
import numpy as np
import re

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)



class Dateien:

    @staticmethod
    def get_fileList(pathFolder : Path) -> List[str]:
        
        dirList : List[str] = os.listdir(pathFolder)
        fileList : List[str] = []

        for entry in dirList:
            if os.path.isfile(pathFolder / entry) == True:
                fileList.append(entry)
        return fileList
    

    
    @staticmethod
    def print_fileList(pathFolder : Path) -> None:
        fileList : List[str] = Dateien.get_fileList(pathFolder)
        for entry in fileList:                                                                  # keep
            print("    " + COLORYELLOW + entry + COLOREND)

            

    @staticmethod  
    def get_lastParticipantNr() -> int: # works
        fileList : List[str] = Dateien.get_fileList(Paths.PATH_JSON_FOLDER)
        name_lastFile : str = fileList[len(fileList)-1]

        matchesPartNr : List[str] = re.findall(r"\d", name_lastFile ) # pick all digits

        fusedMatch = ""
        for match in  matchesPartNr:
            fusedMatch += match

        lastParticipantNr : int = int( fusedMatch )
        return lastParticipantNr

    @staticmethod # works
    def generate_nextParticipantNr() -> int:
        return (Dateien.get_lastParticipantNr() + 1)
