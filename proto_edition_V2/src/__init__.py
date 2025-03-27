from Globals import Globals
from Paths import Paths
from Sequences import Sequences
from Participant import Participant

import freefield
import slab

from typing import List
from pathlib import Path
import numpy as np
import sys
import time
import random
import inspect



COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)




#class Main:

#

if __name__ == "__main__":

    #proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
    #            ['RX81', 'RX8', Paths.PATH_RCX],
    #           ['RX82', 'RX8', Paths.PATH_RCX]]
    #
    #freefield.initialize('dome', device=proc_list)


    p = Participant(1)
    print(p.blockShiftDict["block0"])













