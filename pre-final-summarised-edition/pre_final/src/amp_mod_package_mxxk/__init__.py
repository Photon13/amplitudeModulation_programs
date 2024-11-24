dataframe erstellen !!!!!


import freefield
import slab

import os
import sys

from Leds import Leds
from Globals import Globals
from SoundsAndSequences import SoundsAndSequences
from SpeakersAndBlocks import SpeakersAndBlocks

n_blocks = Globals.n_blocks
n_subblocks = Globals.n_subblocks

soundList = SoundsAndSequences.generate_soundSnippets()

target_list = SpeakersAndBlocks.assign_targets()

df_shiftOccurences = [] #### ????


for i in range(blocks):
    target = target_list[i]
    Leds.turn_targetLed_on(target)
    SpeakersAndBlocks.write_speakers(soundList, shiftOccurence)
    input = input("Block jetzt starten?")
    freefield.play(kind='zBusA')





shiftOccurence = SoundsAndSequences.assign_occurenceShift()
df_shiftOccurences.append [shiftOccurence] #### ??????

