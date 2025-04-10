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

def run_block(target):
    Tests.test_threeSpeakers(Globals.N_SUBBLOCKS, [23.0, 41.0, 57.0], shift=True)
    Led.turnOn_targetLed_forTimeIntervall(target, Globals.N_SUBBLOCKS)

def wait_4secs():
    ende = time.time() + 4
    while True:
        if( time.time()>= ende):
            #Led.turnOff_allLeds()
            break




proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
             ['RX81', 'RX8', Paths.PATH_RCX],
             ['RX82', 'RX8', Paths.PATH_RCX]]

freefield.initialize('dome', device = proc_list)



#Tests.test_allLeds()

#run_block("right")
#run_block("left")
#run_block("middle")
#run_block("both")



#x = "right"
#shiftOccurrence = [x,x,x,x,x, x,x,x,x,x]
#Sprecher.writeToAndTrigger_speakers(["left", "middle", "right"], Globals.FAM_LIST, shiftOccurrence)
#Led.turnOn_targetLed_forTimeIntervall(x, 10)
#wait_4secs()