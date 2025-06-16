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

    identifier : str = "participant_test2" # CAVE: underscore!
    expType : str =    "testLeds"

    ampRiseRange : List[float] = [0.15, 0.3] # all inclusive :D
    ampRiseValue : float = 0.3
    

    # \\\ HELP \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|
    validParticipants : List[str] = ["participant_1", "participant_2", "participant_3", "participant_4" ]
    validExpTypes : List[str] =     ["preTest", "mainExp", "demo", "testSingleSpeaker", "testLeds"      ]
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
        # tested online: length correct (126sec)

        for i in range( 1 ): # n repeats
            nrSeq = Generator.generate_nrSeqs_mainExp(Main.ampRiseValue)[0]

            Freifeld.writeToSpeaker( "Left", Fams.famB, nrSeq )
            Freifeld.sendTrigger_afterShortDelay()
            CommonHelpFunctions.waitForXSeconds( len(nrSeq) )

            CommonHelpFunctions.waitForXSeconds(2)
        

    @staticmethod
    def testLeds() -> None: 
        CommonHelpFunctions.waitForXSeconds(5)
        targets = ["left", "middle", "right", "both"]
        for i in range(len(targets)):
            t = targets[i]
        #for t in targets:
            Freifeld.turnTargetLedOn(t)
            CommonHelpFunctions.waitForXSeconds(2)
            Freifeld.turnAllLedsOff()
            CommonHelpFunctions.waitForXSeconds(2)
 

    @staticmethod
    def demo() -> None: 
        famsLMR = [Fams.famA, Fams.famB, Fams.famC]
        for i in range( 4 ): # n repeats
            nrSeqsLMR = Generator.generate_nrSeqs_mainExp(Main.ampRiseValue)

            Freifeld.writeToAllSpeakers(famsLMR, nrSeqsLMR)
            Freifeld.sendTrigger_afterShortDelay()
            CommonHelpFunctions.waitForXSeconds( len(nrSeqsLMR[0]) )

            CommonHelpFunctions.waitForXSeconds(2)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    @staticmethod
    def preTest() -> None:
        # tested offline: length block correct (336sec)
          
        blockDict : dict = {}
        fileName : str = f"{Main.identifier}_blockDict_preTest.txt"
        
        blockDict["ampRiseRange"]  = Main.ampRiseRange
        blockDict["famsLMR"]       = Main.tryToUsePreAssignedFams()
        #__________________________________________________________________________#
        
        [nrSeq, zeroSeq]    = Generator.generate_nrSeqs_preTest( Main.ampRiseRange )
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

# !!!! MONKEY PATCH !!!! #
Freifeld.PATH_RCX = Path(os.getcwd()) /"data"/"rcx"/"V7.rcx" #_test
#Freifeld.PATH_RCX = Path(os.getcwd()) /"data"/"rcx"/"V7_test.rcx" #_test
  # does actually override Freifeld.PATH_RCX for the whole runtime (-> also the following Freifeld.init_FF() uses the patched value))
# !!!! MONKEY PATCH !!!! #

#bei V7_test.rcx blinkt bit 2 (bei nutzung rx81 oder rx82)
# bei V7_rcx blinken korrekte bits (bei nutzung rx81 oder rx82)


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
elif( Main.expType == "testLeds"):                  #
    Main.testLeds()                                 #
#---------------------------------------------------#
freefield.halt()    #
#-------------------#