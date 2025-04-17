from Globals import Globals

from typing import List
import random
import numpy as np
import sys

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)



class Sequences:


    @staticmethod
    def gen_shiftOccurrence_withoutShifts(n_subblocks : int) -> List[str]:
        shiftOccurrence : List[str] = ["none"]
        for i in range(1, n_subblocks):
            shiftOccurrence.append("none")
        return shiftOccurrence
    
    @staticmethod
    def gen_shiftOccurrence(n_subblocks : int) -> List[str]:
        shiftOccurrence : List[str] = ["none"]
        for i in range(1, n_subblocks):
            shiftOccurrence.append(random.choice(["left", "middle", "right"]))
        return shiftOccurrence
    
    @staticmethod
    def generate_blockShiftDict(n_subblocks : int):
        blockShiftDict : dict = {}
        for i in range(Globals.N_BLOCKS):
            blockShiftDict[f"block{i}"] = Sequences.gen_shiftOccurrence(n_subblocks)
        return blockShiftDict
    


    
    @staticmethod
    def gen_shiftPossList() -> List[List[int]]:
        poss1 = [2, 1, 1, 1]        
        poss2 = [1, 2, 1, 1]        
        poss3 = [1, 1, 2, 1]        
        poss4 = [2, 1, 2, 1] 

        return [poss1, poss2, poss3, poss4]

    @staticmethod
    def gen_nrSeq(position : str, shiftOccurrence : List[str]):
        shiftPossList = Sequences.gen_shiftPossList()
        nrSeq : List[int] = [1,1,1,1]
        for i in range(1, len(shiftOccurrence)):
            if(shiftOccurrence[i] == position):
                poss = random.choice(shiftPossList)
                for nr in poss:
                    nrSeq.append(nr)
            else:
                for nr in [1,1,1,1]:
                    nrSeq.append(nr)
        nrSeq = np.array(nrSeq).astype('int32')
        return nrSeq




    @staticmethod
    def generate_random_targetList() -> List[str]: 
        targetList : List[str] = []  
        k = int(Globals.N_BLOCKS / 4)                                       
        targetList.extend( k*["left"])
        targetList.extend( k*["right"])
        targetList.extend( k*["middle"])
        targetList.extend( k*["both"])
        targetList = random.sample(targetList, k = Globals.N_BLOCKS)

        return targetList




    @staticmethod
    def gen_randomFamList(famList : List[float]) -> List[float]:
        if( len(famList) != 3):
            print(COLORRED + "CAVE: Nr of fams does not equal 3! " + COLOREND + gen_randomFamList())
            sys.exit()
        return random.sample(famList, k=3)
    



    @staticmethod
    def gen_ampRise(ampRiseList : List[float]):
        return np.array(ampRiseList).astype('float64')


