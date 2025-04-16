from Dateien import Dateien
from Experiment import Experiment
from Globals import Globals
from Led import Led
from Logs import Logs
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
from pathlib import Path
import json
import time




COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)



class Init_Experiment:

    @staticmethod
    def run_testBlock(participant : Participant, position : str):
        Sprecher.writeToAndTrigger_speakers( positionen = Globals.POSITIONEN, famList = participant.famList, shiftOccurrence = Sequences.gen_shiftOccurrence(participant.n_subblocks))

        print(COLORPURPLE + f"TestBlock {position} is running." + COLOREND)
        Led.turnOn_targetLed_forTimeIntervall( target = position, n_subblocks = participant.n_subblocks)



    @staticmethod
    def run_block(blockNr : int, participant : Participant):
        Sprecher.writeToAndTrigger_speakers( positionen = Globals.POSITIONEN, famList = participant.famList, shiftOccurrence = participant.blockShiftDict[f"block{blockNr}"])

        print(COLORPURPLE + f"Block{i} is running." + COLOREND)
        Led.turnOn_targetLed_forTimeIntervall( target = participant.targetList[blockNr], n_subblocks = participant.n_subblocks)
        
        Logs.writeToLog_blockDone(participant.nr, i)


#_________________________________________________________________________

proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
             ['RX81', 'RX8', Paths.PATH_RCX],
             ['RX82', 'RX8', Paths.PATH_RCX]]

freefield.initialize('dome', device = proc_list)

#________________________________________________________________________


###########################
participantNr : int = 666 # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
###########################


jsonPath : Path = Paths.get_fileName_jsonParticipant(participantNr)
if jsonPath.exists() == True: #works
    with open(jsonPath, "r") as file:
        jsonData = json.load(file) # type data = dict
    participant = Participant(participantNr)
    participant.__dict__ = jsonData
    print(COLORRED + "Participant reinitiated" + COLOREND)

else: #works
    participant = Participant(participantNr)
    with open( jsonPath, "w") as file:
        json.dump( participant.__dict__, file, indent=4)
    Logs.writeToLog_participantCreated(participant.nr)
    print(COLORRED + "Creating new participant." + COLOREND)


######################
blockToStartWith = 0 # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
######################


while True:
    inp = input(COLORBLUE + "Start experiment? [yes]: " + COLOREND)
    if( inp.lower() == "yes"):
        break

# all leds on for showing position and let them just identify
# the different streams for some secs
# evt without shifts

positions : List[str] = ["left", "middle", "right", "both"]
for position in positions:
    
    Init_Experiment.run_testBlock(participant, position)

    ende = time.time() + 4
    while True:
        if( time.time()>= ende):
            break 

for i in range(blockToStartWith, len(participant.targetList), 2):
    
    Init_Experiment.run_block(i, participant)

    ende = time.time() + 4
    while True:
        if( time.time()>= ende):
             break

    Init_Experiment.run_block((i+1), participant)
    
# write to log exp done?
print("Experiment done.")

    














