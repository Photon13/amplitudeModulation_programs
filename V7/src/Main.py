# txt generation for pretest scores

from Freifeld import Freifeld
from CommonHelpFunctions import CommonHelpFunctions
from Generator import Generator
from Dateien import Dateien
from Fams import Fams

from typing import List
import freefield
from pathlib import Path
import os




class Main:

    identifier : str = "preTestTest010725" # CAVE: underscore!
    expType : str =    "preTest"

    ampRiseRange : List[float] = [0.5, 0.6] # all inclusive :D #[0.15, 0.3]
    ampRiseValue : float = 1.5 #0.3 #0.4
    

    # \\\ HELP \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|
    validParticipants : List[str] = ["participant_1", "participant_2", "participant_3", "participant_4" ]
    validExpTypes : List[str] =     ["preTest", "mainExp", "demo", "testAllSpeakers", "testSingleSpeaker", "testLeds"]
    # \\\ HELP \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|




    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# >>>>> --------------------------------------------------------------------------- # >>>>> 

    @staticmethod #works
    def tryToUsePreAssignedFams() -> List[float]:
        if Main.identifier in Main.validParticipants:
            famsLMR : List[float] = Fams.famCombinationsDictLMR[Main.identifier]
        else:
            famsLMR : List[float] = [Fams.famA, Fams.famB, Fams.famC]
        return famsLMR

    @staticmethod #works
    def tryToComment():
        while True:
            inp1 = input(Dateien.COLORCYAN + "Create Comment? [yes/no]: " + Dateien.COLOREND)
            if( inp1.lower() == "yes"):
                Dateien.comment(Main.identifier, Main.expType)
                break
            elif( inp1.lower() == "no"):
                break

# >>>>> --------------------------------------------------------------------------- # >>>>> 
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    @staticmethod #works
    def testSingleSpeaker() -> None: 
        # tested online: duration correct
        zeroSeq = Generator.generateListOfZeros(20)
        Freifeld.writeToSpeaker( "Left", Fams.famB, zeroSeq )
        Freifeld.sendTrigger_afterShortDelay()
        CommonHelpFunctions.waitForXSeconds( len(zeroSeq) )

    @staticmethod #works
    def testAllSpeakers() -> None: 
        # tested online: duration correct
        zeroSeq = Generator.generateListOfZeros(20)
        Freifeld.writeToSpeaker( "Left",   Fams.famA, zeroSeq )
        Freifeld.writeToSpeaker( "Middle", Fams.famB, zeroSeq )
        Freifeld.writeToSpeaker( "Right",  Fams.famC, zeroSeq )
        Freifeld.sendTrigger_afterShortDelay()
        CommonHelpFunctions.waitForXSeconds( len(zeroSeq) )
        

    @staticmethod
    def testLeds() -> None: 
        CommonHelpFunctions.waitForXSeconds(0)
        targets = ["left", "middle", "right", "both"]
        for i in range(len(targets)):
            t = targets[i]
            Freifeld.turnTargetLedOn(t)
            CommonHelpFunctions.waitForXSeconds(2)
            Freifeld.turnAllLedsOff()
            CommonHelpFunctions.waitForXSeconds(2)
 

    @staticmethod #works
    def demo() -> None: 
        # tested online: duration correct
        duration = 20
        nrSeq = Generator.generate_nrSeq_withShifts(duration, Main.ampRiseValue)
        zeroSeq = Generator.generateListOfZeros( len(nrSeq) )

        Freifeld.writeToSpeaker( "Left",   Fams.famA, nrSeq )
        Freifeld.writeToSpeaker( "Middle", Fams.famB, zeroSeq )
        Freifeld.writeToSpeaker( "Right",  Fams.famC, zeroSeq )
    
        Freifeld.sendTrigger_afterShortDelay()
        CommonHelpFunctions.waitForXSeconds( len(nrSeq) )

        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    @staticmethod #works
    def preTest() -> None:
        # tested online: duration correct
          
        blockDict : dict = {}
        fileName : str = f"{Main.identifier}_blockDict_preTest.txt"
        
        blockDict["ampRiseRange"]  = Main.ampRiseRange
        blockDict["famsLMR"]       = Main.tryToUsePreAssignedFams()
        #__________________________________________________________________________#
        
        nrSeq   = Generator.generate_nrSeq_preTest( Main.ampRiseRange )
        zeroSeq = Generator.generateListOfZeros( len(nrSeq) )
        print(nrSeq) ###

        blockDict["nrSeq"]  = nrSeq 
        Dateien.write_Json( fileName, blockDict )
        #__________________________________________________________________________#
        
        Freifeld.writeToAllSpeakers( blockDict["famsLMR"], [nrSeq, zeroSeq, zeroSeq] )
        Freifeld.sendTrigger_afterShortDelay()
        CommonHelpFunctions.waitForXSeconds( len(nrSeq) )

        Main.tryToComment()
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    
    @staticmethod 
    def mainExp() -> None: 
        # tested offline: created blockDict correct
        #                 length block correct (96sec)

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
            Dateien.write_Json( fileName, blockDict ) #override!
            #_______________________________________________________________________#
            
            Freifeld.turnTargetLedOn( blockDict["targetList"][blockNr] )
            Freifeld.writeToAllSpeakers( blockDict["famsLMR"], nrSeqsLMR )
            Freifeld.sendTrigger_afterShortDelay()

            CommonHelpFunctions.waitForXSeconds( len(nrSeqsLMR[0]) )
            Freifeld.turnAllLedsOff()

            Main.tryToComment()
            inp : str = input("Continue with next block? [any]: ") ###
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#






#-------------------#
Freifeld.init_FF()  #
#---------------------------------------------------#
if( Main.expType == "preTest" ):                    #
    Main.preTest()                                  #
                                                    #
elif( Main.expType == "mainExp" ):                  #
    Main.mainExp()                                  #
                                                    #
elif( Main.expType == "demo"):                      #
    Main.demo()                                     #
                                                    #
elif( Main.expType == "testSingleSpeaker"):         #
    Main.testSingleSpeaker()                        #
                                                    #
elif( Main.expType == "testAllSpeakers"):           #
    Main.testAllSpeakers()                          #
                                                    #
elif( Main.expType == "testLeds"):                  #
    Main.testLeds()                                 #
#---------------------------------------------------#
freefield.halt()    #
#-------------------#
