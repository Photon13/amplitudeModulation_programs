from typing import List

from Globals import Globals

class FreqComb:

    FREQ_COMBS : List[str] = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]

    @staticmethod
    def get_fams_fromFreqComb( freqComb : str ) -> List[float]:
        famA = Globals.FAM_A
        famB = Globals.FAM_B
        famC = Globals.FAM_C
        
        famsLMR_per_freqCond : dict = {
            "ABC" : [ famA, famB, famC ],
            "ACB" : [ famA, famC, famB ],

            "BAC" : [ famB, famA, famC ],
            "BCA" : [ famB, famC, famA ],

            "CAB" : [ famC, famA, famB ],
            "CBA" : [ famC, famB, famA ] 
        }
        return famsLMR_per_freqCond[ freqComb ]
    

class Conditions:

    CONDITIONS : List[str] = ["left", "middle", "right", "both"]


class Trials:

    TRIALS : List[str] = ["1", "2", "3"]