# Interpreter : z.B. freefield

from Participant import Participant
from Globals import Globals
from Noise import Noise
from TestMethods import TestMethods
from Led import Led
from Sprecher import Sprecher
from Experiment import Experiment

import freefield

import numpy as np
import sys
import time
import random

from typing import List

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLOREND = '\033[0m'
COLORPURPLE = "\033[1;35m"

np.set_printoptions(linewidth = 200)




class Main:

    @staticmethod  
    def run_mainExperiment( participantNr : int, globals : object, blockToStartWith : int = 0) -> None:
        """ Create Json if it does not exist yet
            Load participant info from Json
            Init processors
            Prepare Sounds
            Run blocks
            ! (default block to start with: block0) """
        
        if( participantNr == 0 or participantNr < 0):
            print( COLORRED + "Invalid participantNr. " + COLOREND)
            sys.exit()

        if( Participant.check_if_Json_exists(participantNr, globals) == False):
            Experiment.wrapper_participantPreparation(participantNr, globals) 
                # creates new Json if it does not exist yet

        participant : object = Participant.init_singleParticipant_fromJson(participantNr, globals)

        Experiment.init_processors()

        dictSoundData : dict = Noise.generate_soundSnippets(participant)
        
        for i in range(blockToStartWith, participant.n_blocks):
            Experiment.run_block(participant, i, dictSoundData)
            
            while True:
                inp : str = input(COLORBLUE + "Continue with next block? [yes]/no: " + COLOREND)
                if inp.lower() == "yes":
                    break










if __name__ == "__main__":

    globals : object = Globals( mode = "testMode" )
    # AENDERN ZU "non-testMode"



    participantNr : int = 1000



    #if( participantNr % 6 == 1 or participantNr % 6 == 2):
    #    x : List[int] = ["b", "a", "c"]
    #    y = ["c", "a", "b"]
    #    pseudoRandomisedFamList = random.choice( [x, y] )
    #    print(pseudoRandomisedFamList)
    #else:
    #    print("FEHLER")

    Main.run_mainExperiment( participantNr, globals, blockToStartWith = 5)

    #if program crashes during experiment:
    #Main.run_mainExperiment( participantNr, globals, blockToStartWith = <> )
        ## enter desired blockNr : int  at <>


