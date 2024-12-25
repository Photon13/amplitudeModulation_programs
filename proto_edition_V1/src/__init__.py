from Participant import Participant
from Globals import Globals
from Noise import Noise
from TestMethods import TestMethods

import numpy as np

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)

if __name__ == "__main__":

    participantNr = 556

    #TestMethods.wrapper_participantPreparation(participantNr)

    participant : object = Participant.init_singleParticipant_fromJson(participantNr)
    dictSoundData : dict = Noise.generate_soundSnippets(participant)
    
    TestMethods.init_processors()

    for i in range(participant.n_blocks):
        TestMethods.run_block(participant, i, dictSoundData)

