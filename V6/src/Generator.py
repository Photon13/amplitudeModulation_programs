import math
from typing import List
import random
import numpy as np
import sys

from Globals import Globals
from GeneratorPreTest import GeneratorPreTest


class Generator:

    @staticmethod
    def gen_blockdict(expType : str, ampRiseRange : List[float]) -> dict:
        """ Generates blockDict containing fams ( adressable as blockDict["fams"]["fam<Position>"],
        targets ( adressable as blockDict["block<nr>"]["target"] ),
        and nrSeqs ( adressable as blockDict["block<nr>"]["nrSeq<Position>"] ) """
        blockDict : dict = {}

        blockDict["n_blocks"] = Globals.N_BLOCKS
        fams : List[float] = GeneratorPreTest.randomlyAssign_fams() # fams manually changed after blockDict generation
        famDict = {
                    "famLeft" : fams[0],
                    "famMiddle" : fams[1],
                    "famRight" : fams[2]
        }
        blockDict["fams"] = famDict

        targetList = GeneratorPreTest.gen_randomisedTargetList() 
        
        for i in range (Globals.N_BLOCKS):
            nrSeqLeft, nrSeqMiddle, nrSeqRight = Generator.get_nrSeqs(expType, ampRiseRange)
            dictBlockX = {
                "target" : targetList[i],
                "nrSeqLeft" : nrSeqLeft,
                "nrSeqMiddle" : nrSeqMiddle,
                "nrSeqRight" : nrSeqRight
            }
            blockDict[f"block{i}"] = dictBlockX

        return blockDict













    def get_positionList(expType : str):
        positionsList : List[str] = []
        snippetTypesList : List[int] = []
        ampRiseValueList : List[float] = []

        if( expType == "preTest" ):
            for i in range(48):
                snippetTypesList.append(1)
            for i in range(32):
                snippetTypesList.append(2)
        else:
            for i in range(15):
                snippetTypesList.append(1)
            for i in range(10):
                snippetTypesList.append(2)

        random.shuffle(snippetTypesList)


        if( expType == "preTest" ):
            for i in range(80): # 48 + 32
                positionsList.append("l")
        else:
            for i in range(25):
                positionsList.append(random.choice(["l","m","r"]))

        if( expType == "preTest" ):
            if( len( possAmpRiseValues != 8)):
                print(Globals.COLORRED + "posAmpRiseValues has wrong length!" + Globals.COLOREND)
            for ampRiseValue in possAmpRiseValues:
                for i in range(8):
                    ampRiseValueList.append(ampRiseValue)
            random.shuffle(ampRiseValueList)
        else:
            for i in range(25): #?
                ampRiseValueList.append(possAmpRiseValues[0])

            ###
        if( snippetType == 1):
                snippet =       [ampRiseValue, 0.0, 0.0]
                antiSnippet =   [0.0, 0.0, 0.0]
        elif( snippetType == 2):
                snippet =       [ampRiseValue, 0.0, 0.0,  0.0, 0.0, 0.0]
                antiSnippet =   [0.0, 0.0, 0.0,  0.0, 0.0, 0.0]






















    @staticmethod
    def get_nrSeqs(ampRiseValueList : List[float], positionList : List[str]):
        """ positionList and ampRiseValueList must have same length"""
            
        nrSeqLeft : List[float] = []
        nrSeqMiddle : List[float] = []
        nrSeqRight : List[float] = []

        for i in range( len(positionList) ):
            pos = positionList[i]
            ampRiseValue = ampRiseValueList[i]

        for pos in positionList:
            snippetType : int = random.choices([1,2], weights = [0.6, 0.4], k=1)[0]
            if( snippetType == 1):
                snippet =       [ampRiseValue, 0.0, 0.0]
                antiSnippet =   [0.0, 0.0, 0.0]
            elif( snippetType == 2):
                snippet =       [ampRiseValue, 0.0, 0.0,  0.0, 0.0, 0.0]
                antiSnippet =   [0.0, 0.0, 0.0,  0.0, 0.0, 0.0]

            if( pos == "l"):
                for s in snippet:
                    nrSeqLeft.append(s)
                for a in antiSnippet:
                    nrSeqMiddle.append(a)
                    nrSeqRight.append(a)
                
            elif( pos == "m"): #keeping it here could safe work if other speakers shall be used
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

        return nrSeqLeft, nrSeqMiddle, nrSeqRight
    


    @staticmethod
    def get_possAmpRiseList(ampRiseRange : List[float], n_ampRiseValues : int = 10) -> List[float]:
        """ take range from start value to end value (both inclusive) and divide it
        to get n values, that are equally spaced;
        if both range values are equal,  """
        if( ampRiseRange[1] > ampRiseRange[0] ):
            diff = ampRiseRange[1] - ampRiseRange[0]
            k = ampRiseRange[0]
        elif( ampRiseRange[1] < ampRiseRange[0] ): 
            diff = ampRiseRange[0] - ampRiseRange[1]
            k = ampRiseRange[1]
        else:
            return [ ampRiseRange[0] ] # only contains 1 value

        possAmpRiseList : List[float] = []
        for i in range ( n_ampRiseValues ):
            possAmpRiseList.append(round(k,3))
            k += diff/9
        # using log values does not seem to make a difference ... spaces stay the same
        return possAmpRiseList