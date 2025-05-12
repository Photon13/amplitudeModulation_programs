from Sprecher_und_Procs import Sprecher_und_Procs
from Dateien_und_Json import Dateien_und_Json
from GeneratorMainExp import GeneratorMainExp
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



class init:

    @staticmethod
    def getBlockDict(expType : str, identifier, ampRise):
        if(expType == "demo"):
            return GeneratorMainExp.gen_blockdict(ampRise) # no json generation or reading
        else:
            return init.readJson_or_genNewBlockDict(expType, identifier, ampRise)

    @staticmethod
    def readJson_or_genNewBlockDict(expType : str, identifier, ampRise):
        exists = Dateien_und_Json.check_whetherJsonExists(f"{identifier}_{expType}.txt")
        if( exists == True ):
            blockDict = Dateien_und_Json.readJson(f"{identifier}_{expType}.txt")
        else:
            if(expType == "preTest"):
                blockDict = GeneratorPreTest.gen_blockdict() # CAVE class
            elif(expType == "mainExp"):
                blockDict = GeneratorMainExp.gen_blockdict(ampRise) # CAVE class
            Dateien_und_Json.export_toJson(blockDict, f"{identifier}_{expType}.txt")
            blockDict = Dateien_und_Json.readJson(f"{identifier}_{expType}.txt")
        return blockDict



    @staticmethod
    def stopUntilYes(message : str):
        inp = input(Globals.COLORCYAN + f"{message} [yes]: " + Globals.COLOREND)
        while True:
            if( inp.lower() == "yes"):
                break

    @staticmethod
    def pauseProgrammForSomeTime(timeIntervall : float):
        end = time.time() + timeIntervall
        while True:
            if( time.time() >= end ):
                break

    @staticmethod
    def relayStart(timeToRelay : float) -> None:
        init.stopUntilYes("Start?")
        init.pauseProgrammForSomeTime(timeToRelay)

    


    @staticmethod
    def waitUntilBlockFinishes(blockDict : dict) -> None:
        duration_block = len(blockDict[f"block{i}"]["nrSeqLeft"])
        init.pauseProgrammForSomeTime(duration_block)

    @staticmethod
    def endBlock_and_startNewBlock(blockDict : dict) -> None:
        init.waitUntilBlockFinishes(blockDict)
        Sprecher_und_Procs.turnAllLedsOff(speakerLedDict)
        if(expType == "mainExp"):
            init.stopUntilYes("Continue with next block?")
        else: 
            init.pauseProgrammForSomeTime(3.0)



#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
expTypes = ["demo", "preTest", "mainExp"]
expType : str = "demo"                          #<<<<

identifier : str = "testAll"
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
if(expType == "demo"):
    ampRise : float = 0.4                   
elif(expType == "preExp"):
    ampRise : float = -666.0
elif(expType == "mainExp"):
    ampRise : float = 0.2                   #<<<<
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§



blockDict = init.getBlockDict(expType, identifier, ampRise)

Sprecher_und_Procs.initFF()
speakerLedDict = Sprecher_und_Procs.pickSpeakersAndLeds()

print( COLORRED + "Remember to start recording!" + COLOREND)
init.relayStart(timeToRelay = 1)        #<<<<

for i in range( blockDict["n_blocks"] ):
    Sprecher_und_Procs.turnTargetLedOn(speakerLedDict, target = blockDict[f"block{i}"]["target"])
    Sprecher_und_Procs.writeToSpeakers_fromBlockDict(speakerLedDict, blockDict, i)
    freefield.play()

    print(blockDict[f"block{i}"]["nrSeqLeft"])
    print(blockDict[f"block{i}"]["nrSeqMiddle"])
    print(blockDict[f"block{i}"]["nrSeqRight"])

    init.endBlock_and_startNewBlock(blockDict)


