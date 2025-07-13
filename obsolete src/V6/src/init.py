from Sprecher_und_Procs import Sprecher_und_Procs
from Dateien_und_Json import Dateien_und_Json
from GeneratorMainExp import GeneratorMainExp
from GeneratorPreTest import GeneratorPreTest

from Globals import Globals

import time
import sys
from typing import List
import freefield

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

# fct for checking spelling expType
# preassign fams
#   -> create blockdict, then change fams, then export json

class Init:

    @staticmethod
    def prepare(expType, identifier, ampRiseRange):
        if(expType == "demo" or "testSingleSpeaker"):
            blockDict = GeneratorMainExp.gen_blockdict(ampRiseRange) #

        elif(expType == "preTest" or "mainExp"):
            blockDict = Init.tryToReadJson(expType, identifier)
            if(blockDict == None):
                print( COLORCYAN + "Generating new blockDict." + COLOREND)
                blockDict = GeneratorPreTest.gen_blockdict(ampRiseRange) #
                Dateien_und_Json.export_toJson(blockDict, f"{identifier}_{expType}.txt")
            else:
                print( COLORCYAN + "BlockDict fetched from memory." + COLOREND)

        else:
            print( COLORRED + "Invalid expType!" + COLOREND)
            sys.exit()

        print( COLORRED + "Remember to start recording!" + COLOREND)
        return blockDict


    @staticmethod
    def tryToReadJson(expType : str, identifier : str):
        exists = Dateien_und_Json.check_whetherJsonExists(f"{identifier}_{expType}.txt")
        if(exists == True):
            blockDict = Dateien_und_Json.readJson(f"{identifier}_{expType}.txt")
            return blockDict
        else:
            return None

    #______________________________________________________________________________________________

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
        Init.stopUntilYes("Start?")
        Init.pauseProgrammForSomeTime(timeToRelay)

    #______________________________________________________________________________________________

    @staticmethod
    def waitUntilBlockFinishes(blockDict : dict) -> None:
        duration_block = len(blockDict[f"block{i}"]["nrSeqLeft"])
        Init.pauseProgrammForSomeTime(duration_block)

    @staticmethod
    def endBlock_and_startNewBlock(blockDict : dict) -> None:
        Init.waitUntilBlockFinishes(blockDict)
        Sprecher_und_Procs.turnAllLedsOff(speakerLedDict)
        if(expType == "mainExp"):
            Init.stopUntilYes("Continue with next block?")
        else: 
            Init.pauseProgrammForSomeTime(3.0)






#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§$$$$
identifier : str = "teeest"                                      #<<<<

expTypes = ["demo", "preTest", "mainExp", "testSingleSpeaker"]
expType : str = "testSingleSpeaker"                              #<<<<
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
if(expType == "demo"):
    ampRiseRange : List[float] = [0.4, 0.4]                  
elif(expType == "preExp"):
    ampRiseRange : List[float] = [0.1, 0.3]
elif(expType == "mainExp"):
    ampRiseRange : List[float] = [0.2, 0.2]                      #<<<<

elif(expType == "testSingleSpeaker"):
    ampRiseRange : List[float] = [0.3, 0.3]
    position = "Right"
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§


Sprecher_und_Procs.initFF()
speakerLedDict = Sprecher_und_Procs.pickSpeakersAndLeds()
blockDict= Init.prepare(expType, identifier, ampRiseRange)

#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
Init.relayStart(timeToRelay = 1)            #<<<<
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§


for i in range( blockDict["n_blocks"] ):

    if((expType == "testSingleSpeaker")):
        Sprecher_und_Procs.turnTargetLedOn(speakerLedDict, position)
        Sprecher_und_Procs.writeToSingleSpeaker(speakerLedDict, blockDict, i, position)
    else:
        Sprecher_und_Procs.turnTargetLedOn(speakerLedDict, blockDict[f"block{i}"]["target"])
        Sprecher_und_Procs.writeToSpeakers_fromBlockDict(speakerLedDict, blockDict, i)

    freefield.play()

    print(blockDict[f"block{i}"]["nrSeqLeft"])
    print(blockDict[f"block{i}"]["nrSeqMiddle"])
    print(blockDict[f"block{i}"]["nrSeqRight"])

    Init.endBlock_and_startNewBlock(blockDict)


