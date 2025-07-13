from Sprecher_und_Procs import Sprecher_und_Procs
from Dateien_und_Json import Dateien_und_Json
from GeneratorPreTest import GeneratorPreTest
from Globals import Globals

import time
import freefield

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

class PreTest:

    @staticmethod
    def prepare_blockDict(identifier) -> dict:
        """ checks whether Json exists,
        returns blockDict from Json if Json exists,
        otherwise a new blockDict is generated, pushed to Json and returned """
        exists = Dateien_und_Json.check_whetherJsonExists(f"{identifier}_preTest.txt")
        if( exists == True ):
            #blockDict = Dateien_und_Json.readJson(f"{identifier}_preTest.txt")
            blockDict = Dateien_und_Json.get_blockDict_fromJson(f"{identifier}_preTest.txt")
        else:
            blockDict = GeneratorPreTest.gen_blockdict() # CAVE class
            Dateien_und_Json.export_toJson(blockDict, f"{identifier}_preTest.txt")
            #blockDict = Dateien_und_Json.readJson(f"{identifier}_preTest.txt")
            blockDict = Dateien_und_Json.get_blockDict_fromJson(f"{identifier}_preTest.txt")
        return blockDict

    @staticmethod
    def relayStart(timeIntervall : float):
        inp = input("Start? [yes]: ")
        while True:
            if( inp.lower() == "yes"):
                break

        end = time.time() + timeIntervall
        while True:
            if( time.time() >= end ):
                break


#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
identifier : str = "testMarkerAnalysis1"        # nickname for participant
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#



Sprecher_und_Procs.initFF()
speakerLedDict = Sprecher_und_Procs.pickSpeakersAndLeds()

blockDict = PreTest.prepare_blockDict(identifier)

print( COLORRED + "Remember to start recording!" + COLOREND)
PreTest.relayStart(timeIntervall = 15)

for i in range( blockDict["n_blocks"] ):
    Sprecher_und_Procs.writeToSpeakers_fromBlockDict(speakerLedDict, blockDict, i)
    freefield.play()
    #run without stop




# "testMarkerAnalysis0" range 0.15 to 0.4 # ok, but 0.4 much to loud
# "testMarkerAnalysis1" range 0.1 to 0.25 # most much to quiet