# fix beating from fams -> probably the 150 ms from rcx are causing this

from Freifeld import Freifeld
from CommonHelpFunctions import CommonHelpFunctions
from Generator import Generator
from Dateien import Dateien


class Main:

    expType = "testSingleSpeaker"
    expTypes = ["preTest", "mainExp", "demo", "testSingleSpeaker", "testLeds"]

    identifier = "testV7_0" #participantX if pre-defined fam combinations shall be used

    ampRiseValue = 0.3
    ampRiseRange = [0.15, 0.3]

    famA = 31.7 #33.0
    famB = 42.1 #43.0
    famC = 52.1 #53.0

    famCombinationsDict : dict = {
        "participant1" :   [famB, famA, famC],
        "participant2" :   [famA, famC, famB],
        "participant3" :   [famC, famA, famB],
        "participant4" :   [famB, famC, famA]
    }


    # block dict
        # check if identifier matches one of the famCombinationDict keys


    def preTest():

    def mainExp():

        n_blocks = 16

        blockDict = {}
        blockDict["n_blocks"] = n_blocks
        targetList = Generator.generate_targetList()
        [famLeft, famMiddle, famRight] = tryToUsePreAssignedFams()

        for blockNr in range( n_blocks ):
            [nrSeqLeft, nrSeqMiddle, nrSeqRight] = Generator.generate_nrSeqs_mainExp(Main.ampRiseValue)
            target = targetList[blockNr]
            blockData = {
                "target"     : target,
                "nrSeqLeft"  : nrSeqLeft,
                "nrSeqMidde" : nrSeqMiddle,
                "nrSeqRight" : nrSeqRight
            }
            Dateien.extentJsonDict(f"{Main.identifier}_mainExp.txt", key = f"block{blockNr}", value = blockData)
            
            Freifeld.writeToSpeaker( "Left",   famLeft,   nrSeqLeft   )
            Freifeld.writeToSpeaker( "Middle", famMiddle, nrSeqMiddle )
            Freifeld.writeToSpeaker( "Right",  famRight,  nrSeqRight  )
            Freifeld.sendTrigger_afterShortDelay()

            CommonHelpFunctions.waitForXSeconds( len(nrSeqLeft) )
            CommonHelpFunctions.waitForXSeconds(2)
            inp : str = input("Continue with next block?") ###

    @staticmethod
    def demo():
        [nrSeqLeft, nrSeqMiddle, nrSeqRight] = Generator.generate_nrSeqs_mainExp(Main.ampRiseValue)
        for i in range( 4 ): # n repeats
            Freifeld.writeToSpeaker( "Left",   Main.famA, nrSeqLeft   )
            Freifeld.writeToSpeaker( "Middle", Main.famB, nrSeqMiddle )
            Freifeld.writeToSpeaker( "Right",  Main.famC, nrSeqRight  )

            Freifeld.sendTrigger_afterShortDelay()
            CommonHelpFunctions.waitForXSeconds( len(nrSeqLeft) )
            CommonHelpFunctions.waitForXSeconds(2)

    @staticmethod
    def testSingleSpeaker():
        nrSeq = Generator.generate_nrSeqs_mainExp(Main.ampRiseValue)[0]
        for i in range( 1 ): # n repeats
            Freifeld.writeToSpeaker( "Left",   Main.famB, nrSeq   )

            Freifeld.sendTrigger_afterShortDelay()
            CommonHelpFunctions.waitForXSeconds( len(nrSeq) )
            CommonHelpFunctions.waitForXSeconds(2)

    @staticmethod
    def testLeds():
        CommonHelpFunctions.waitForXSeconds(15)
        targets = ["left", "middle", "right", "both"]
        for t in targets:
            Freifeld.turnTargetLedOn(t)
            CommonHelpFunctions.waitForXSeconds(1)
            Freifeld.turnAllLedsOff()




Freifeld.init_FF()

if( Main.expType == "preTest" ):
    Main.preTest()
elif( Main.expType == "mainExp" ):
    Main.mainExp()
elif( Main.expType == "demo"):
    Main.demo()
elif( Main.expType == "testSingleSpeaker"):
    Main.testSingleSpeaker()
elif( Main.expType == "testLeds"):
    Main.testLeds()

