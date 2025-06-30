import json
import os
import time
import sys

from Fams import Fams


class Dateien:

    COLORBLUE   = '\33[34m'
    COLORGREEN = "\033[0;32m"
    COLORRED    = '\33[31m'
    COLORCYAN = '\033[36m'
    COLORPURPLE = '\033[35m'
    COLORYELLOW = '\033[33m'
    COLORFAT = '\033[1m'
    COLOREND = '\033[0m'


#_____GENERAL_____#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    @staticmethod #works
    def read_Json(fileName : str) -> None:
        pathFile : str = f"json/{fileName}"
        if os.path.exists(pathFile):
            with open(pathFile, "r") as f:
                data = json.load(f)
        return data
    
    @staticmethod #works
    def write_Json(fileName : str, data) -> None:
        pathFile : str = f"json/{fileName}"
        with open(pathFile, "w") as f:
            json.dump(data, f, indent = 4)

    #_____________________________________________________________________________________________________________

    @staticmethod #works
    def append_TxtFile(pathFile : str, text : str) -> None:
        with open(pathFile, "a") as f:  # CAVE: creates file if does not exist yet
            f.write(f"\n{text}")        # CAVE: inserts line break

    @staticmethod #works
    def print_TxtFileContent(pathFile : str) -> None:
        with open(pathFile, "r") as f:
            content = f.read()
        print( Dateien.COLORYELLOW + f"{content}" + Dateien.COLOREND )


#_____SPECIFIC_____#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    @staticmethod #works
    def comment(identifier : str, expType : str) -> None:
        comment = input(Dateien.COLORGREEN + "Comment: " + Dateien.COLOREND)
        text : str = ""
        text += f"{time.strftime('%Y-%m-%d %H:%M:%S')} \n"
        text += f"Identifier: {identifier}\n"
        text += f"Experiment Type: {expType}\n"
        text += f"\n"
        text += f"Comment: {comment}\n"
        text += f"--------------------------------------------------------\n"

        pathFile : str = f"logs/logComments.txt"
        Dateien.append_TxtFile(pathFile, text)





        
