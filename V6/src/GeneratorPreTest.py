import math
from typing import List
import random
import numpy as np

class GeneratorPreTest:


    @staticmethod
    def print_possAmpRiseList(start = 1.1, end = 1.3) -> None:
        diff = end - start

        k = start
        for i in range (10):
            print(f"{round(k,3)}", end = ", ")
            k += diff/9

    @staticmethod
    def get_possAmpRiseList() -> List[float]:
        possAmpRiseList : List[float] = [1.1, 1.122, 1.144, 1.167, 1.189, 1.211, 1.233, 1.256, 1.278, 1.3]
        return possAmpRiseList


    @staticmethod
    def get_nrSeqs():

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
            length = random.choices([1,2,3], weights = [0.7, 0.3, 0.1], k=1)[0]

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

        nrSeqLeft = np.array(nrSeqLeft).astype('float64') # ca. 247 secs
        nrSeqMiddle = np.array(nrSeqLeft).astype('float64')
        nrSeqRight = np.array(nrSeqLeft).astype('float64')

        return nrSeqLeft, nrSeqMiddle, nrSeqRight # seems to work


# check whether num seq containing floats is compatible with rcx!

# nrSeq must be saved somehow
# e.g. separate function taking nrSeq output as input (or calling the fct. above) and exporting nrSeqs as json

# target list also still needed in V6