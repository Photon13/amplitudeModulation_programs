from Dateien import Dateien
from Experiment import Experiment
from Globals import Globals
from Led import Led
from Participant import Participant
from Paths import Paths
from Sequences import Sequences
from Settings import Settings
from Sprecher import Sprecher
from Tests import Tests

import freefield

from typing import List
import random
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

class Init_Maik:

    def run_testBlocks(participant : Participant):
            # single speaker:
            Sprecher.writeToAndTrigger_speakers( positionen = Globals.POSITIONEN, 
                                                 famList = participant.famList, 
                                                 shiftOccurrence = Sequences.gen_shiftOccurrence(participant.n_subblocks)
            )
            Led.turnOn_targetLed_forTimeIntervall( target = random.choice(["left", "middle", "right"]), 
                                                   n_subblocks = participant.n_subblocks
            )
            print(COLORPURPLE + f"TestBlocks are running." + COLOREND)

            # both speakers:
            Sprecher.writeToAndTrigger_speakers( positionen = Globals.POSITIONEN, 
                                                 famList = participant.famList, 
                                                 shiftOccurrence = Sequences.gen_shiftOccurrence(participant.n_subblocks)
            )
            
            Led.turnOn_targetLed_forTimeIntervall( target = "both", 
                                                   n_subblocks = participant.n_subblocks
            )




    def run_block(blockNr : int, participant : Participant):
            Sprecher.writeToAndTrigger_speakers( positionen = Globals.POSITIONEN, 
                                                 famList = participant.famList, 
                                                 shiftOccurrence = participant.blockShiftDict[f"block{blockNr}"]
            )
            Led.turnOn_targetLed_forTimeIntervall( target = participant.targetList[blockNr], 
                                                   n_subblocks = participant.n_subblocks
            )
            print(COLORPURPLE + f"Block{i} is running." + COLOREND)
            # write to log




#################################################
proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
             ['RX81', 'RX8', Paths.PATH_RCX],
             ['RX82', 'RX8', Paths.PATH_RCX]]

freefield.initialize('dome', device = proc_list)

participantNr : int = 0
participant = Participant(participantNr)

famList = Globals.FAM_LIST
participant.setManually_famList(famList)


while True:
    inp = input(COLORBLUE + "Start experiment? [yes]:" + COLOREND)
    if( inp.lower() == "yes"):
        break

Tests.test_allLeds()
Init_Maik.run_testBlocks(participant)

i = 0
imax = len(participant.targetList)-1 # index of last target
while(i <= imax):
    j = 0
    while( j < 2): # run superblock (4 blocks)
        Init_Maik.run_block(i, participant)
        i += 1
        j += 1

    if( i == imax + 1):
        print(COLORGREEN + "Experiment finished." + COLOREND)
    else:
        while True:
            inp = input(COLORBLUE + "Continue with next block? [yes]:" + COLOREND)
            if( inp.lower() == "yes"):
                break