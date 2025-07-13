from pathlib import Path
import json
import os

from GeneratorPreTest import GeneratorPreTest

class Dateien_und_Json:

    @staticmethod
    def export_toJson(data, identifier : str): #works
        """ Write data to json txt file, 
        possible data e.g. dict or str """
        
        with open(f"json\\{identifier}.txt", "w") as f: # relative path used, because Path -> str causes problems (i.e. PATH_CWD can't be used)
            json.dump(data, f, indent = 4)

    @staticmethod
    def get_blockDict_fromJson(identifier : str ): #works
        """ Get content of json txt file,
        possible data e.g. dict or str """
        with open(f"json\\{identifier}.txt", "r") as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def check_whetherJsonExists(identifier : str) -> bool: #works
        return os.path.exists(f"json\\{identifier}.txt")
    
# TEST:
# identifier = "dictTest"
# Dateien_und_Json.export_toJson(GeneratorPreTest.gen_blockdict(), identifier)
# blockDict = Dateien_und_Json.get_blockDict_fromJson(identifier)
# print(blockDict)