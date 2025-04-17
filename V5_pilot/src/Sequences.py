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
    def gen_ampRise(ampRiseList : List[float]):
        return np.array(ampRiseList).astype('float64')


