from Sprecher_und_Procs import Sprecher_und_Procs
from Dateien_und_Json import Dateien_und_Json
from GeneratorMainExp import GeneratorMainExp

from Globals import Globals

import time
import freefield

class MainExp:

    @staticmethod
    def prepare_blockDict(identifier : str, ampRise : float) -> dict:
        """ checks whether Json exists,
        returns blockDict from Json if Json exists,
        otherwise a new blockDict is generated, pushed to Json and returned """
        exists = Dateien_und_Json.check_whetherJsonExists(f"{identifier}_mainExp.txt")
        if( exists == True ):
            blockDict = Dateien_und_Json.readJson(f"{identifier}_mainExp.txt")
        else:
            blockDict = GeneratorMainExp.gen_blockdict(ampRise) # CAVE class
            Dateien_und_Json.export_toJson(blockDict, f"{identifier}_mainExp.txt")
            blockDict = Dateien_und_Json.readJson(f"{identifier}_mainExp.txt")
        return blockDict



#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
ampRise : float = 0.15      # 0.X !
identifier : str = ""       # nickname for participant
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#

 

Sprecher_und_Procs.initFF()
speakerLedDict = Sprecher_und_Procs.pickSpeakersAndLeds()

blockDict = MainExp.prepare_blockDict(identifier, ampRise)

for i in range( blockDict["n_blocks"] ):
    Sprecher_und_Procs.turnTargetLedOn(speakerLedDict, target = blockDict[f"block{i}"]["target"])
    Sprecher_und_Procs.writeToSpeakers_fromBlockDict(speakerLedDict, blockDict, i)
    freefield.play()

    duration_block = len(blockDict[f"block{i}"]["nrSeqLeft"])

    while True:
        if( time.time() >= (time.time() + duration_block) ):
            break
    Sprecher_und_Procs.turnAllLedsOff()
    inp = input(Globals.COLORBLUE + "Continue with next block?" + Globals.COLOREND)
