import math
from typing import List
import random
import numpy as np
import sys

from Globals import Globals
from GeneratorPreTest import GeneratorPreTest



class GeneratorMainExp:
    # Directly taken from GeneratorPreTest
        # GeneratorPreTest.randomlyAssign_fams()
        # GeneratorPreTest.gen_randomisedTargetList()
        # GeneratorPreTest.print_possAmpRiseList(start = 1.1, end = 1.3)
        # GeneratorPreTest.get_possAmpRiseList()

    @staticmethod
    def get_nrSeqs(ampRiseRange : List[float]):
        """ Give parameter ampRiseRange as [rise, rise] """
        ampRise = ampRiseRange[0]
        # Create List of Lists, latter one containing shift and some sec no shift
        x : List[List[float]] = []
        for i in range(6):
            x.append( [ampRise, 0.0] )
        for i in range(8):
            x.append( [ampRise, 0.0, 0.0] )
        for i in range(6):
            x.append( [ampRise, 0.0, 0.0, 0.0] )
        random.shuffle( x ) # randomise order of snippets

        # 8*2sec + 8*3sec + 8*4sec
        # = 16sec + 24sec + 32sec = 62sec (+ 3sec empty # added later)
        # -> per block: 65 sec

        y : List[float] = []
        for lst in x: # for each snippet:
            for nr in lst: # for each float in snippet: take float and append
                y.append( nr )
    
        nrSeqLeft : List[float] = []
        nrSeqMiddle : List[float] = []
        nrSeqRight : List[float] = []

        for i in range(3): # first 3 sec no shift
            nrSeqLeft.append( 0.0 )
            nrSeqMiddle.append( 0.0 )
            nrSeqRight.append( 0.0 )

        possPositionsShift = ["l", "m", "r"]
        for entry in y: # for each sec
            if( entry == 0.0 ): # no shift at all (i.e. in none of the streams)
                nrSeqLeft.append( entry )
                nrSeqMiddle.append( entry )
                nrSeqRight.append( entry )

            else: # if shift shall occur
                shiftPos = random.choice( possPositionsShift ) # randomly choose a position
                # chosen position gets shift value, the others get 0.0
                if( shiftPos == "l"):
                    nrSeqLeft.append( entry )
                    nrSeqMiddle.append( 0.0 )
                    nrSeqRight.append( 0.0 )

                elif( shiftPos == "m"):
                    nrSeqLeft.append( 0.0 )
                    nrSeqMiddle.append( entry )
                    nrSeqRight.append( 0.0 )

                elif( shiftPos == "r"):
                    nrSeqLeft.append( 0.0 )
                    nrSeqMiddle.append( 0.0 )
                    nrSeqRight.append( entry )

        return nrSeqLeft, nrSeqMiddle, nrSeqRight



    @staticmethod
    def gen_blockdict(ampRiseRange : List[str]) -> dict:
        """ Generates blockDict containing fams ( adressable as blockDict["fams"]["fam<Position>"],
        targets ( adressable as blockDict["block<nr>"]["target"] ),
        and nrSeqs ( adressable as blockDict["block<nr>"]["nrSeq<Position>"] ) """
        blockDict : dict = {}

        blockDict["n_blocks"] = Globals.N_BLOCKS
        fams = GeneratorPreTest.randomlyAssign_fams() # List[float]
        famDict = {
                    "famLeft" : fams[0],
                    "famMiddle" : fams[1],
                    "famRight" : fams[2]
        }
        blockDict["fams"] = famDict

        targetList = GeneratorPreTest.gen_randomisedTargetList() 
        
        for i in range (Globals.N_BLOCKS):
            nrSeqLeft, nrSeqMiddle, nrSeqRight = GeneratorMainExp.get_nrSeqs(ampRiseRange) #
            dictBlockX = {
                "target" : targetList[i],
                "nrSeqLeft" : nrSeqLeft,
                "nrSeqMiddle" : nrSeqMiddle,
                "nrSeqRight" : nrSeqRight
            }
            blockDict[f"block{i}"] = dictBlockX

        return blockDict
    

#TEST:
#nrSeqLeft, nrSeqMiddle, nrSeqRight = GeneratorMainExp.get_nrSeqs([7.7, 7.7])
#print("\n")
#print(nrSeqLeft)
#print(nrSeqMiddle)
#print(nrSeqRight)
#print(len(nrSeqLeft))
#print(len(nrSeqMiddle))
#print(len(nrSeqRight))
#print(len(np.array(nrSeqLeft).astype('float64')))


