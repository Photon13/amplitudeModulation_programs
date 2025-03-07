# Interpreter : z.B. freefield

from Participant import Participant
from Globals import Globals
from Noise import Noise
from TestMethods import TestMethods
from Led import Led
from Sprecher import Sprecher
from Experiment import Experiment
from Dateien import Dateien

import freefield

import numpy as np
import sys
import time
import random

from typing import List
from pathlib import Path


COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLOREND = '\033[0m'
COLORPURPLE = "\033[1;35m"
COLORYELLOW = '\033[33m'

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



def generate_participantNR_basedOnFreq() -> int:
    """ generation of participant nr for AM Test: 
        participantNr is generated as <famA><famB><famC><shift>,
    #                           e.g. 37114 """

    participantNr : str = ""
    participantNr += str(Globals.FAM_A_BASE)
    participantNr += str(Globals.FAM_B_BASE)
    participantNr += str(Globals.FAM_C_BASE)
    participantNr += str(Globals.SHIFT_A)
    participantNr += str(Globals.SHIFT_B)
    participantNr += str(Globals.SHIFT_C)

    participantNr : int = int(participantNr)

    return participantNr






if __name__ == "__main__":

    """ keep: block should always be activated """

    #__________INIT_GLOBALS________________________________________________________________

    mode = "testMode"                                                                       # ENABLE FOR all TESTs
    
    #mode = "non-testMode"                                                                  # ENABLE FOR eXPERIMENT
                                                                       
    globals : object = Globals( mode )                                                      # keep
    
    #__________LIST_ALL_EXISTING_JSON_FILES________________________________________________

    pathJsonMode : Path = globals.get_pathJsonFolder()                                      # keep
    jsonList : List[str] = Dateien.get_fileList(pathJsonMode)
    for entry in jsonList:                                                                  # keep
        print("    " + COLORYELLOW + entry + COLOREND)
    
    #__________PARTICIPANT_NR______________________________________________________________

    #participantNr : int = generate_participantNR_basedOnFreq() # für AM test               # ENABLE FOR ***AM TEST***
        
    participantNr : int = 1004 # normal assignment manually                             # ENABLE FOR eXPERIMENT

    #__________CONFIRM_PARTICIPANT_NR______________________________________________________

    print("    " + COLORBLUE + f"Current participantNr == {participantNr}" + COLOREND)      # keep
    while True: 
        inp = input("    " + COLORGREEN + "Continue [yes]? " + COLOREND)                    # keep
        if inp.lower() == "yes":
            break

    #_________START_EXPERIMENT_____________________________________________________________

    #Main.run_mainExperiment( participantNr, globals)                                       # keep, DEFAULT = 0 !

    Main.run_mainExperiment( participantNr, globals, blockToStartWith = 3 )                 # ENABLE IF PROGRAM CRASHES
        ## enter desired blockNr at blockToStartWith





