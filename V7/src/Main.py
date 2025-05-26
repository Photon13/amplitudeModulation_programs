#zbus trigger needed for test leds?
# txt generation for pretest scores

#review length mainExp again -> change to 90 secs??

# test length expTypes
# measure volume dB again

# what if pretest shall be done twice? -> keep fams somehow (?)

# fix beating from fams -> probably the 150 ms from rcx are causing this

from Freifeld import Freifeld
from CommonHelpFunctions import CommonHelpFunctions
from Generator import Generator
from Dateien import Dateien
from Fams import Fams

from typing import List
import re


class Main:

    identifier : str = "participant_0" # CAVE: underscore!
    expType : str =    "testLeds"

    ampRiseRange : List[float] = [0.15, 0.3]
    ampRiseValue : float = 0.3
    

    # \\\ HELP \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|
    validParticipants : List[str] = ["participant_1", "participant_2", "participant_3", "participant_4" ]
    validExpTypes : List[str] =     ["preTest", "mainExp", "demo", "testSingleSpeaker", "testLeds"      ]
    # \\\ HELP \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|


# >>>>> --------------------------------------------------------------------------- # >>>>> 

    @staticmethod
    def tryToUsePreAssignedFams() -> List[float]:
        if Main.identifier in Main.validParticipants:
            famsLMR : List[float] = Fams.famCombinationsDictLMR[Main.identifier]
        else:
            famsLMR : List[float] = [Fams.famA, Fams.famB, Fams.famC]
        return famsLMR

    @staticmethod
    def writeToLogs():
        Dateien.comment()

# >>>>> --------------------------------------------------------------------------- # >>>>>
    
    @staticmethod #works #126sec
    def testSingleSpeaker() -> None: #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
        for i in range( 1 ): # n repeats
            nrSeq = Generator.generate_nrSeqs_mainExp(Main.ampRiseValue)[0]

            Freifeld.writeToSpeaker( "Left", Fams.famB, nrSeq )
            Freifeld.sendTrigger_afterShortDelay()
            CommonHelpFunctions.waitForXSeconds( len(nrSeq) )

            CommonHelpFunctions.waitForXSeconds(2)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#


    @staticmethod
    def testLeds() -> None: #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
        CommonHelpFunctions.waitForXSeconds(5)
        targets = ["left", "middle", "right", "both"]
        for t in targets:
            Freifeld.turnTargetLedOn(t)
            CommonHelpFunctions.waitForXSeconds(1)
            Freifeld.turnAllLedsOff()
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#



    @staticmethod
    def demo() -> None: #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
        famsLMR = [Fams.famA, Fams.famB, Fams.famC]
        for i in range( 4 ): # n repeats
            nrSeqsLMR = Generator.generate_nrSeqs_mainExp(Main.ampRiseValue)

            Freifeld.writeToAllSpeakers(famsLMR, nrSeqsLMR)
            Freifeld.sendTrigger_afterShortDelay()
            CommonHelpFunctions.waitForXSeconds( len(nrSeqsLMR[0]) )

            CommonHelpFunctions.waitForXSeconds(2)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#



    @staticmethod
    def preTest() -> None: #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
        blockDict : dict = {}
        fileName : str = f"{Main.identifier}_blockDict_preTest.txt"
        
        blockDict["ampRiseRange"]  = Main.ampRiseRange
        blockDict["famsLMR"]       = Main.tryToUsePreAssignedFams()
        #__________________________________________________________________________#
        
        [nrSeq, zeroSeq]    = Generator.generate_nrSeqs_preTest( Main.ampRiseRange )
        blockDict["nrSeq"]  = nrSeq 
        Dateien.write_Json( fileName, blockDict )
        #__________________________________________________________________________#
        
        Freifeld.writeToAllSpeakers( blockDict["famsLMR"], [nrSeq, zeroSeq, zeroSeq] )
        Freifeld.sendTrigger_afterShortDelay()

        CommonHelpFunctions.waitForXSeconds( len(nrSeq) )
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    
    
    
    @staticmethod
    def mainExp() -> None: #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
        blockDict : dict = {}
        fileName : str = f"{Main.identifier}_blockDict_mainExp.txt"
        
        blockDict["n_blocks"]    = 16
        blockDict["ampRise"]     = Main.ampRiseValue
        blockDict["famsLMR"]     = Main.tryToUsePreAssignedFams()
        blockDict["targetList"]  = Generator.generate_targetList()
        #___________________________________________________________________________#
        
        for blockNr in range( blockDict["n_blocks"] ):
            
            nrSeqsLMR = Generator.generate_nrSeqs_mainExp( Main.ampRiseValue )
            
            blockDict[f"block{blockNr}"] = { "target"     : blockDict["targetList"][blockNr], 
                                             "nrSeqLeft"  : nrSeqsLMR[0], 
                                             "nrSeqMidde" : nrSeqsLMR[1], 
                                             "nrSeqRight" : nrSeqsLMR[2]   
            }
            Dateien.write_Json( fileName, blockDict )
            #_______________________________________________________________________#
            
            Freifeld.turnTargetLedOn( blockDict["targetList"][blockNr] )
            Freifeld.writeToAllSpeakers( blockDict["famsLMR"], nrSeqsLMR )
            Freifeld.sendTrigger_afterShortDelay()

            CommonHelpFunctions.waitForXSeconds( len(nrSeqsLMR[0]) )
            Freifeld.turnAllLedsOff()
            
            CommonHelpFunctions.waitForXSeconds(2)
            inp : str = input("Continue with next block? [any]") ###
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#






#-------------------#
Freifeld.init_FF()  #
#-----------------------------------------------#
if( Main.expType == "preTest" ):                #
    Main.preTest()                              #
    Main.writeToLogs()                          #
                                                #
elif( Main.expType == "mainExp" ):              #
    Main.mainExp()                              #
    Main.writeToLogs()                          #
                                                #
elif( Main.expType == "demo"):                  #
    Main.demo()                                 #
                                                #
elif( Main.expType == "testSingleSpeaker"):     #
    Main.testSingleSpeaker()                    #
                                                #
elif( Main.expType == "testLeds"):              #
    Main.testLeds()                             #
#-----------------------------------------------#
