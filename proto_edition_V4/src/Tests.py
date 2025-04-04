from Globals import Globals
from Sequences import Sequences
from Experiment import Experiment
from Sprecher import Sprecher

from typing import List
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



class Tests:


    @staticmethod
    def test_singleSpeaker(position : str, n_subblocks : int, freq : float, shift : bool):
        positionen = [position]
        if( shift == True):
            shiftOccurrence : List[str]= Sequences.gen_shiftOccurrence(n_subblocks)
        else:
            shiftOccurrence : List[str]= Sequences.gen_shiftOccurrence_withoutshifts(n_subblocks)
        
        Sprecher.writeToAndTrigger_speakers(positionen, 
                                            [freq], 
                                            shiftOccurrence
        )

    @staticmethod
    def test_threeSpeakers(n_subblocks : int, freqs : List[float], shift : bool):
        positionen = ["left", "middle", "right"]
        if( shift == True):
            shiftOccurrence : List[str]= Sequences.gen_shiftOccurrence(n_subblocks)
        else:
            shiftOccurrence : List[str]= Sequences.gen_shiftOccurrence_withoutshifts(n_subblocks)
        Sprecher.writeToAndTrigger_speakers(positionen, 
                                            Sequences.gen_randomFamList(freqs), 
                                            shiftOccurrence
        )





