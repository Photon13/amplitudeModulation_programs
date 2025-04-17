import freefield
from typing import List

from Globals import Globals
from Paths import Paths
from Sequences import Sequences
from Sprecher import Sprecher

proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
             ['RX81', 'RX8', Paths.PATH_RCX],
             ['RX82', 'RX8', Paths.PATH_RCX]]

freefield.initialize('dome', device = proc_list)

positionen : List[str] = ["left", "middle", "right"]
shiftOccurrence : List[str]= Sequences.gen_shiftOccurrence(n_subblocks = 4)
ampRiseList = [0.4, 0.3, 0.2, 0.1]
Sprecher.writeToSpeakers(positionen, ampRiseList, Globals.FAM_LIST, shiftOccurrence)
freefield.play()

#shifts shall only be in single speaker
# ampRise not properly sent
