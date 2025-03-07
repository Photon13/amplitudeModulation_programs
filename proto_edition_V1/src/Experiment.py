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
COLORPURPLE = "\033[1;35m"

np.set_printoptions(linewidth = 200)




class Experiment:

    @staticmethod
    def init_processors() -> None:

        proc_list = [['RP2', 'RP2', Globals.PATH_RCX_FILE],
                    ['RX81', 'RX8', Globals.PATH_RCX_FILE],
                    ['RX82', 'RX8', Globals.PATH_RCX_FILE]]

        freefield.initialize('dome', device=proc_list)




    @staticmethod
    def wrapper_participantPreparation(participantNr : int, globals : object) -> None:

        participant = Participant(participantNr)
        participant.export_participantInstance_toJson(participant, globals)
        print(COLORGREEN + "Participant information successfully prepared. " + COLOREND 
              + "Message from wrapper_participantPreparation(participantNr : int))")



    @staticmethod
    def run_block(participant : object, blockNr : int, dictSoundData : dict) -> None:

        print(COLORGREEN + f"Preparing block_{blockNr} ..." + COLOREND)

        target : str = participant.targetList[blockNr]
        Led.turn_targetLed_on(target)

        Sprecher.wrapper_writeTo_speakers(participant, blockNr, dictSoundData)


        timeToWait1 : int = 1  # waits 1 sec to avoid lag for loading data onto rcx // possibly abundant
        stopTime1 : float = time.time() + timeToWait1

        while True:
            if time.time() > stopTime1:

                freefield.play(kind = "zBusA")
                print(COLORGREEN + f"Block_{blockNr} started." + COLOREND)
                break


        timeToWait2 : int = participant.n_subblocks *4 *2  # each subblock 4 sec
        stopTime2 : float = time.time() + timeToWait2      ### CAVE: DURATION SNIPPET SUDDENLY 2 SEC

        while True:
            if time.time() > stopTime2:

                Led.turn_all_leds_off()
                print(COLORGREEN + f"Block_{blockNr} finished." + COLOREND)
                break