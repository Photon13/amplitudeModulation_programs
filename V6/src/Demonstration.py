from Sprecher_und_Procs import Sprecher_und_Procs
from Dateien_und_Json import Dateien_und_Json
from GeneratorMainExp import GeneratorMainExp

from Globals import Globals

import time
import freefield


#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
ampRise : float = 0.15      # 0.X !
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#

 

Sprecher_und_Procs.initFF()
speakerLedDict = Sprecher_und_Procs.pickSpeakersAndLeds()

blockDict = GeneratorMainExp.gen_blockdict(ampRise) # only difference to MainExp -> drops blockDict after usage

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