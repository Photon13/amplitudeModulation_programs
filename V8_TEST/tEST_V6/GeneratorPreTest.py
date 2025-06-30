import math
from typing import List
import random
import numpy as np
import sys

from Globals import Globals



class GeneratorPreTest:

    @staticmethod
    def randomlyAssign_fams() -> List[float]:
        fams = Globals.FAM_LIST
        random.shuffle(fams)
        return fams

    @staticmethod
    def gen_randomisedTargetList() -> List[str]:
        n_trialsPerTarget = 5
        if( n_trialsPerTarget * 4 != Globals.N_BLOCKS ):
            print( Globals.COLORRED + "fatal: Number of blocks in gen_randomisedTargetList() does not match Globals.N_BLOCKS" + Globals.COLOREND)
            sys.exit()
        possTargets : List[str] = ["left", "middle", "right", "both"]
        targetList : List[str] = []
        for target in possTargets:
            for i in range( n_trialsPerTarget ):
                targetList.append( target )
        random.shuffle( targetList )
        # prevent target of block0 from being "both":
        while True:
            if( targetList[0] != "both"):
                break
            else:
                random.shuffle(targetList) 
        return targetList


    @staticmethod
    def print_possAmpRiseList(start = 1.1, end = 1.3) -> None:
        """ take range from start value to end value (both inclusive) and divide it
        to get 10 values, that are equally spaced; print result, return None
        default: start = 110% amplitude, end = 130% amplitude """
        diff = end - start

        k = start
        for i in range (10):
            print(f"{round(k,3)}", end = ", ")
            k += diff/9
        # using log values does not seem to make a difference ... spaces stay the same



    @staticmethod
    def get_possAmpRiseList() -> List[float]:
        """ returns all possible amplitude values for nrseq in case a shift occurs;
        to modify range of amplitude values, new values must be manually pasted;
        current range is 110% to 130% amplitude """
        #possAmpRiseList : List[float] = [0.1, 0.122, 0.144, 0.167, 0.189, 0.211, 0.233, 0.256, 0.278, 0.3]
        possAmpRiseList : List[float] = [0.15, 0.178, 0.206, 0.233, 0.261, 0.289, 0.317, 0.344, 0.372, 0.4]

        return possAmpRiseList



    @staticmethod
    def get_nrSeqs():
        """ returns np.NDArrays[float] of nrSeqLeft, nrSeqMiddle and nrSeqRight;
        each containing all possible ampRise values (as 1.10 etc.) 10 times, respectively;
        ampRise values are separated by 1-3 0.0's (p = 0.7, 0.3, 0.1) """

        possAmpRiseList : List[float] = GeneratorPreTest.get_possAmpRiseList()

        values : List[float] = []
        for rise in possAmpRiseList:
            for i in range(10):
                values.append(rise)
        random.shuffle(values) # works so far
    
        nrSeqLeft : List[float] = []
        nrSeqMiddle : List[float] = []
        nrSeqRight : List[float] = []

        for value in values:
            pos = random.choice(["l", "m", "r"])
            length = random.choices([1,2,3], weights = [0.5, 0.4, 0.1], k=1)[0]

            if( length == 1):
                snippet =       [value, 0.0]
                antiSnippet =   [0.0,   0.0]
            elif( length == 2):
                snippet =       [value, 0.0, 0.0]
                antiSnippet =   [0.0,   0.0, 0.0]
            elif( length == 3):
                snippet =       [value, 0.0, 0.0, 0.0]
                antiSnippet =   [0.0,   0.0, 0.0, 0.0]

            if( pos == "l"):
                for s in snippet:
                    nrSeqLeft.append(s)
                for a in antiSnippet:
                    nrSeqMiddle.append(a)
                    nrSeqRight.append(a)
            
            elif( pos == "m"):
                for s in snippet:
                    nrSeqMiddle.append(s)
                for a in antiSnippet:
                    nrSeqLeft.append(a)
                    nrSeqRight.append(a)

            elif( pos == "r"):
                for s in snippet:
                    nrSeqRight.append(s)
                for a in antiSnippet:
                    nrSeqLeft.append(a)
                    nrSeqMiddle.append(a)

        #nrSeqLeft = np.array(nrSeqLeft).astype('float64') # ca. 247 secs
        #nrSeqMiddle = np.array(nrSeqLeft).astype('float64')
        #nrSeqRight = np.array(nrSeqLeft).astype('float64')

        return nrSeqLeft, nrSeqMiddle, nrSeqRight # seems to work



    @staticmethod
    def gen_blockdict() -> dict:
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
            nrSeqLeft, nrSeqMiddle, nrSeqRight = GeneratorPreTest.get_nrSeqs()
            dictBlockX = {
                "target" : targetList[i],
                "nrSeqLeft" : nrSeqLeft,
                "nrSeqMiddle" : nrSeqMiddle,
                "nrSeqRight" : nrSeqRight
            }
            blockDict[f"block{i}"] = dictBlockX

        return blockDict



GeneratorPreTest.print_possAmpRiseList(start = 0.15, end = 0.4)
