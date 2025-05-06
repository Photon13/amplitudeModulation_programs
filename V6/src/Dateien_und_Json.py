from pathlib import Path
import json
import os

from GeneratorPreTest import GeneratorPreTest
from Paths import Paths

class Dateien_und_Json:

    @staticmethod #works
    def get_pathBVFile(fileName : str):
        """ Returns path of BrainVisionReceorder file as str;
        fileName must contain extension (.vmrk)"""
        return str( Paths.PATH_FOLDER_BRAINVISION_RECORDER / fileName)
    

    
    @staticmethod #works
    def get_pathJsonFile(fileName : str):
        """ Returns path of json file as str;
        fileName must contain extension (.txt)"""
        return str( Paths.PATH_FOLDER_JSON / fileName)

    @staticmethod #works
    def export_toJson(data, fileName : str): 
        """ Write data to json txt file, 
        possible data e.g. dict or str """
        pathFile : str= Dateien_und_Json.get_pathJsonFile(fileName)
        with open(pathFile, "w") as f: # relative path used, because Path -> str causes problems (i.e. PATH_CWD can't be used)
            json.dump(data, f, indent = 4)

    @staticmethod #works
    def readJson(fileName : str): 
        """ Get content of json txt file,
        possible data e.g. dict or str """
        pathFile : str = Dateien_und_Json.get_pathJsonFile(fileName)
        with open(pathFile, "r") as f:
            data = json.load(f)
        return data
    
    @staticmethod #works
    def check_whetherJsonExists(fileName : str) -> bool: 
        return os.path.exists( Dateien_und_Json.get_pathJsonFile(fileName ) )
    
#TEST:
#identifier = "dictTest"
#Dateien_und_Json.export_toJson(GeneratorPreTest.gen_blockdict(), f"{identifier}.txt")
#blockDict = Dateien_und_Json.readJson(f"{identifier}.txt")
#print(blockDict)