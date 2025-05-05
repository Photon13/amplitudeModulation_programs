from Sprecher_und_Procs import Sprecher_und_Procs
from Dateien_und_Json import Dateien_und_Json
from GeneratorPreTest import GeneratorPreTest
from Globals import Globals

import time
import freefield

class PreTest:

    @staticmethod
    def prepare_blockDict(identifier) -> dict:
        """ checks whether Json exists,
        returns blockDict from Json if Json exists,
        otherwise a new blockDict is generated, pushed to Json and returned """
        exists = Dateien_und_Json.check_whetherJsonExists(identifier)
        if( exists == True ):
            blockDict = Dateien_und_Json.get_blockDict_fromJson(identifier)
        else:
            blockDict = GeneratorPreTest.gen_blockdict() # CAVE class
            Dateien_und_Json.export_toJson(blockDict, identifier)
            blockDict = Dateien_und_Json.get_blockDict_fromJson(identifier)
        return blockDict



identifier : str = "test0" # name of json file (without extension)
identifier = f"{identifier}_preTest" # CAVE ending

Sprecher_und_Procs.initFF()
speakerLedDict = Sprecher_und_Procs.pickSpeakersAndLeds()

blockDict = PreTest.prepare_blockDict(identifier)

for i in range( blockDict["n_blocks"] ):
    Sprecher_und_Procs.writeToSpeakers_fromBlockDict(speakerLedDict, blockDict, i)
    freefield.play()
    # no leds
    #inp = input(Globals.COLORBLUE + "Continue with next block?" + Globals.COLOREND)



#To do:
    # change to single speaker for test
    # shifts still to quiet


