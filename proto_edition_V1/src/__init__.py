# Interpreter : z.B. freefield

from Participant import Participant
from Globals import Globals
from Noise import Noise
from TestMethods import TestMethods
from Led import Led
from Sprecher import Sprecher

import freefield

import numpy as np
import sys
import time
import random

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)




class Experiment:

    @staticmethod
    def init_processors() -> None:

        proc_list = [['RP2', 'RP2', Globals.PATH_RCX_FILE],
                    ['RX81', 'RX8', Globals.PATH_RCX_FILE],
                    ['RX82', 'RX8', Globals.PATH_RCX_FILE]]

        freefield.initialize('dome', device=proc_list)




    @staticmethod
    def wrapper_participantPreparation(participantNr : int) -> None:

        participant = Participant(participantNr)
        participant.export_participantInstance_toJson()
        print(COLORGREEN + "Participant information successfully prepared. " + COLOREND 
              + "Message from wrapper_participantPreparation(participantNr : int))")




    @staticmethod
    def run_block(participant : object, blockNr : int, dictSoundData : dict) -> None:

        print(COLORGREEN + f"Preparing block_{blockNr} ..." + COLOREND)

        target : str = participant.targetList[blockNr]
        Led.turn_targetLed_on(target)
        print("TargetLed turned on. ")

        print("Writing to speakers ... ")
        Sprecher.wrapper_writeTo_speakers(participant, blockNr, dictSoundData)


        timeToWait : int = 1  # waits 1 sec to avoid lag for loading data onto rcx // possibly abundant
        stopTime : float = time.time() + timeToWait

        while True:
            if time.time() > stopTime:

                freefield.play(kind = "zBusA")
                print(COLORGREEN + f"Block_{blockNr} started." + COLOREND)
                break


        timeToWait : int = participant.n_subblocks * 4  # each subblock 4 sec
        stopTime : float = time.time() + timeToWait

        while True:
            if time.time() > stopTime:

                Led.turn_all_leds_off()
                print(COLORGREEN + f"Block_{blockNr} finished." + COLOREND)
                break




class Main:
            
    def run_mainExperiment( participantNr : int) -> None:
        
        if( participantNr == 0 or participantNr < 0):
            print( COLORRED + "Invalid participantNr. " + COLOREND)
            sys.exit()

        if( Participant.check_if_Json_exists(participantNr) == False):
            Experiment.wrapper_participantPreparation(participantNr) 
                # creates new Json if it does not exist yet

        participant : object = Participant.init_singleParticipant_fromJson(participantNr)

        Experiment.init_processors()

        dictSoundData : dict = Noise.generate_soundSnippets(participant)
        
        for i in range(participant.n_blocks):
            Experiment.run_block(participant, i, dictSoundData)
            
            while True:
                inp : str = input(COLORBLUE + "Continue with next block? [yes]/no: " + COLOREND)
                if inp.lower() == "yes":
                    break




if __name__ == "__main__":
    Main.run_mainExperiment( participantNr = 3)





