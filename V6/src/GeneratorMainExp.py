import math
from typing import List
import random
import numpy as np
import sys

from Globals import Globals
from GeneratorPreTest import GeneratorPreTest



class GeneratorMainExp:
    # Take directly from GeneratorPreTest
        # GeneratorPreTest.randomlyAssign_fams()
        # GeneratorPreTest.gen_randomisedTargetList()
        # GeneratorPreTest.print_possAmpRiseList(start = 1.1, end = 1.3)
        # GeneratorPreTest.get_possAmpRiseList()

    @staticmethod
    def get_nrSeqs(ampRise : float): #works but parameter is annoying

        x : List[List[float]] = []
        for i in range(3):
            x.append( [ampRise, 0.0] )
        for i in range(3):
            x.append( [ampRise, 0.0, 0.0] )
        for i in range(3):
            x.append( [ampRise, 0.0, 0.0, 0.0] )
        random.shuffle( x )

        y : List[float] = []
        for lst in x:
            for nr in lst:
                y.append( nr )
    
        nrSeqLeft : List[float] = []
        nrSeqMiddle : List[float] = []
        nrSeqRight : List[float] = []

        possPositionsShift = ["l", "m", "r"]

        for entry in y:
            if( entry == 0.0 ):
                nrSeqLeft.append( entry )
                nrSeqMiddle.append( entry )
                nrSeqRight.append( entry )
            else: 
                shiftPos = random.choice( possPositionsShift )
                if( shiftPos == "l"):
                    nrSeqLeft.append( entry )
                    nrSeqMiddle.append( 0.0 )
                    nrSeqRight.append( 0.0 )
                elif( shiftPos == "m"):
                    nrSeqLeft.append( 0.0 )
                    nrSeqMiddle.append( entry )
                    nrSeqMiddle.append( 0.0 )
                elif( shiftPos == "r"):
                    nrSeqLeft.append( 0.0 )
                    nrSeqMiddle.append( 0.0 )
                    nrSeqRight.append( entry )
        return nrSeqLeft, nrSeqMiddle, nrSeqRight



    @staticmethod
    def gen_blockdict(ampRise: str) -> dict:
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
            nrSeqLeft, nrSeqMiddle, nrSeqRight = GeneratorMainExp.get_nrSeqs(ampRise)
            dictBlockX = {
                "target" : targetList[i],
                "nrSeqLeft" : nrSeqLeft,
                "nrSeqMiddle" : nrSeqMiddle,
                "nrSeqRight" : nrSeqRight
            }
            blockDict[f"block{i}"] = dictBlockX

        return blockDict
    

#TEST:
nrSeqLeft, nrSeqMiddle, nrSeqRight = GeneratorMainExp.get_nrSeqs(7.7)
print(nrSeqLeft)
print(len(nrSeqLeft))
print(len(np.array(nrSeqLeft).astype('float64')))
#print(nrSeqMiddle)
#print(nrSeqRight)

