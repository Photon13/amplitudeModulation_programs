import json
import os

COLORRED    = '\33[31m'
COLOREND = '\033[0m'



class Dateien:

    @staticmethod
    def extentJsonDict(fileName : str, key, value) -> None:
        blockDict = Dateien.readFromJson(fileName)
        blockDict[key] = value
        Dateien.overrideJson(fileName, blockDict)

    @staticmethod
    def readFromJson(fileName : str):
        pathFile : str = f"json/{fileName}"
        with open(pathFile, "r") as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def overrideJson(fileName : str, data):
        pathFile : str = f"json/{fileName}"
        if( Dateien.fileExists == True ):
            with open(pathFile, "w") as f:
                json.dump(data, f, indent = 4)

    @staticmethod
    def fileExists(pathFile : str) -> bool:
        if( os.path.exists(pathFile) ):
           return True
        else:
            print(COLORRED + "File does not exist!" + COLOREND)
            return False
        
