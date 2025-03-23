# Interpreter : z.B. freefield

    # Rcx: Flags sollten eingefügt werden, falls ein Syntax Fehler im Code ist,
    # wäre es evt. schneller über die Flags sichtbar, welche Werte falsch sind

    # mne count nr epochs (alternative: count nr zBus triggers)
    # for security

# ToDo:
# test 1 Hz
# find button trigger
# create stimuli for BrainVision, create own setup
# test other button



from Participant import Participant
from Globals import Globals
from Noise import Noise
from TestMethods import TestMethods
from Led import Led
from Sprecher import Sprecher
from Experiment import Experiment
from Dateien import Dateien

import freefield
import slab

import numpy as np
import sys
import time
import random
import inspect

from typing import List
from pathlib import Path


COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

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

        print("\n" + "    " + COLORBLUE + f"BlockToStartWith is {blockToStartWith}." + COLOREND)
        while True:
            inp = input("    " + COLORGREEN + "Continue [yes]? " + COLOREND)
            if inp.lower() == "yes":
                break


        participant : object = Participant.init_singleParticipant_fromJson(participantNr, globals)

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



    def main():
        """ keep: block should always be activated """

        #__________INIT_GLOBALS________________________________________________________________

        #mode = "testMode"                                                                       # ENABLE FOR all TESTs
        
        mode = "non-testMode"                                                                  # ENABLE FOR eXPERIMENT
                                                                        
        globals : object = Globals( mode )                                                      # keep
        
        #__________LIST_ALL_EXISTING_JSON_FILES________________________________________________

        pathJsonMode : Path = Globals.get_pathJsonFolder(globals.mode)                                      # keep
        jsonList : List[str] = Dateien.get_fileList(pathJsonMode)
        for entry in jsonList:                                                                  # keep
            print("    " + COLORYELLOW + entry + COLOREND)
        
        #__________PARTICIPANT_NR______________________________________________________________

        #participantNr : int = Main.generate_participantNR_basedOnFreq() # für AM test          # ENABLE FOR ***AM TEST***
            
        participantNr : int = 1007 # normal assignment manually                                 # ENABLE FOR eXPERIMENT

        #__________CONFIRM_PARTICIPANT_NR______________________________________________________

        print("    " + COLORBLUE + f"Current participantNr is {participantNr}" + COLOREND)      # keep
        while True: 
            inp = input("    " + COLORGREEN + "Continue [yes]? " + COLOREND)                    # keep
            if inp.lower() == "yes":
                print("\n")
                break

        #_________START_EXPERIMENT_____________________________________________________________

        #Main.run_mainExperiment( participantNr, globals)                                       # keep, DEFAULT = 0 !

        Main.run_mainExperiment( participantNr, globals, blockToStartWith = 3 )                 # ENABLE IF PROGRAM CRASHES
            ## enter desired blockNr at blockToStartWith





if __name__ == "__main__":

    proc_list = [['RP2', 'RP2', Globals.PATH_RCX_FILE],
                ['RX81', 'RX8', Globals.PATH_RCX_FILE],
                ['RX82', 'RX8', Globals.PATH_RCX_FILE]]

    freefield.initialize('dome', device=proc_list)


    Main.main()
    #TestMethods.test_speakers(["left", "middle"], [13, 17], True, True, 4)












