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
    def generate_targetList() -> List[str]: 
        targetList : List[str] = []  
        k = int(Globals.N_BLOCKS / 4)                                       
        targetList.extend( k*["left"])
        targetList.extend( k*["right"])
        targetList.extend( k*["middle"])
        targetList.extend( k*["both"])
        targetList = random.sample(targetList, k = 16)

        return targetList




    @staticmethod
    def gen_randomFamList(famList : List[float]) -> List[float]:
        if( len(famList) != 3):
            print(COLORRED + "CAVE: Nr of fams does not equal 3! " + COLOREND + gen_randomFamList())
            sys.exit()
        return random.sample(famList, k=3)
    
    @staticmethod
    def generate_famList(participantNr : int) -> List[float]: # works
        """ for each 6 participants:
            [40.0, 35.3, 44.7]      # [B,A,C]
            [35.3, 40.0, 44.7]      # [A,B,C]
            [35.3, 44.7, 40.0]      # [A,C,B]
            [44.7, 35.3, 40.0]      # [C,A,B]
            [44.7, 40.0, 35.3]      # [C,B,A]
            [40.0, 44.7, 35.3]      # [B,C,A]
        """

        famList : List[float] = [1.0, 1.0, 1.0] # just as placeholder

        if( (participantNr+2) %3 == 0):          # [1, 4, 7, 10, 13, 16, 19, 22, ...]
            famList[1] = Globals.FAM_A_BASE      # *A*
            if( (participantNr+2) %6 != 0):      # [1, 7, 13, 19, ...]
                famList[0] = Globals.FAM_B_BASE  # BAC
                famList[2] = Globals.FAM_C_BASE  # CAB
            else:                                # [4, 10, 16, 22, ...]
                famList[0] = Globals.FAM_C_BASE  # CAB
                famList[2] = Globals.FAM_B_BASE  # BAC

        elif( (participantNr+1) %3 == 0):        # [2, 5, 8, 11, 14, 17, 20, 23, ...]
            famList[1] = Globals.FAM_B_BASE      # *B*
            if( (participantNr+1) %6 != 0):      # [2, 8, 14, 20, ...]
                famList[0] = Globals.FAM_A_BASE  # ABC
                famList[2] = Globals.FAM_C_BASE  # CBA
            else:                                # [5, 11, 17, 23, ...]
                famList[0] = Globals.FAM_C_BASE
                famList[2] = Globals.FAM_A_BASE

        elif( (participantNr+0) %3 == 0):        # [3, 6, 9, 12, 15, 18, 21, 24, ...]
            famList[1] = Globals.FAM_C_BASE      # *C*
            if( (participantNr+0) %6 != 0):      # [3, 9, 15, 21, ...]
                famList[0] = Globals.FAM_A_BASE  # ACB
                famList[2] = Globals.FAM_B_BASE  # BCA
            else:                                # [6, 12, 18, 24, ...]
                famList[0] = Globals.FAM_B_BASE  # BCA
                famList[2] = Globals.FAM_A_BASE  # ACB

        return famList

