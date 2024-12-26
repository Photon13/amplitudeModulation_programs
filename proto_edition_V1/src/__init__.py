# Interpreter : z.B. freefield

from Participant import Participant
from Globals import Globals
from Noise import Noise
from TestMethods import TestMethods
from Led import Led

import freefield
import numpy as np

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)

if __name__ == "__main__":

    participantNr = 111

    #TestMethods.wrapper_participantPreparation(participantNr)

    TestMethods.init_processors()

    participant : object = Participant.init_singleParticipant_fromJson(participantNr)
    dictSoundData : dict = Noise.generate_soundSnippets(participant)
    
    

    for i in range(participant.n_blocks):
        TestMethods.run_block(participant, i, dictSoundData)
        
        while True:
            inp : str = input(COLORBLUE + "Continue with next block? [yes]/no: " + COLOREND)
            if inp.lower() == "yes":
                break

