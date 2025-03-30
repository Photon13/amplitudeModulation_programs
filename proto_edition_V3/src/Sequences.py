from Globals import Globals

from typing import List
import random
import numpy as np

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
    def generate_targetList( self ) -> List[str]: 
        targetList : List[str] = []                                          
        targetList.append(random.choice(["left", "middle", "right"]))  # 0.block            
        targetList.append("both")                                      # 1.block

        helpList : List[str] = []
        helpList.extend( 4*["left"])
        helpList.extend( 4*["right"])
        helpList.extend( 4*["middle"])
        helpList.extend( 4*["both"])
        helpList = random.sample(helpList, k = 16)

        targetList = targetList + helpList

        if(len(targetList != Globals.N_BLOCKS)):
            print(COLORRED + "CAVE: nr of targets does not equal nr of blocks! " + COLOREND + "Check Sequences.generate_targetList()")
            sys.exit()
        
        return targetList



    @staticmethod
    def generate_nrSeq(n_subblocks):
        """ 1: no shift
            2: shift (higher amplitude)
            for all speakers """

        poss1 = [2, 1, 1, 1]        # should work, because Schmitt is open for 200 ms if 2 comes
        poss2 = [1, 2, 1, 1]        # but marker for shift start is sent immediately, when 2 comes
        poss3 = [1, 1, 2, 1]        # thus, participants have almost 1 sec until next shift might occur to press button
        poss4 = [2, 1, 2, 1]        
        poss5 = [1, 2, 2, 1]        # last sec always shift-less
        poss6 = [2, 2, 1, 1]
        
        shiftPoss = [poss1, poss2, poss3, poss4, poss5, poss6]

        nrSeq = [1, 1, 1, 1] # 0.subblock no shift
        for i in range(1, n_subblocks):
            nrs = random.choice(shiftPoss)
            for nr in nrs:
                nrSeq.append(nr)

        nrSeq = np.array(nrSeq).astype('int32')
        return nrSeq


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