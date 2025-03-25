from typing import List
import random
import numpy as np
import sys

from Globals import Globals
from Experiment import Experiment
from Sprecher import Sprecher

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'



class Test_amPinknoise:

    def testSpeakers2(positions : List[str], frequencies : List[int], n_subblocks : int = 0):
        leftSpeaker, middleSpeaker, rightSpeaker = Sprecher.get_speakerCoordinates()

        if( len(positions) != len(frequencies)):
            print( COLORRED + "Frequencies must have same number of entries as positions!" 
                            + COLOREND + "TestMethods.test_pureAMpinknoise()")
            sys.exit()

        nrSeq = Test_amPinknoise.gen_nrSeq(4)
        print(nrSeq)

        # shifOccurence obsolete
        # freqs must still be safed for participant






    def gen_nrSeq(n_subblocks):
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





  