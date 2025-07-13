import freefield
from typing import List
import numpy as np
import time

from Globals import Globals
from Paths import Paths
from Sequences import Sequences
from Sprecher_und_Procs import Sprecher_und_Procs
from ParticipantConstants import ParticipantConstants
from Generator import Generator


ampRiseList = Generator.gen_ampRiseArray_mainExperment()# CAVE: must be changed
    #n_shifts = 22 # mean length 60 sec (1 poss rise value)

Sprecher_und_Procs.initFF()
speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

for i in range(Globals.N_BLOCKS):
    shiftOccurrence = ParticipantConstants.SHIFTOCCURRENCE_01234[ParticipantConstants.currentParticipantNr][f"block{i}"]
    target =  ParticipantConstants.TARGET_LIST_01234[ParticipantConstants.currentParticipantNr][i]

    Sprecher_und_Procs.turnTargetLedOn(leds, target) # PROBLEM?
    Sprecher_und_Procs.writeToAllSpeakers(speakers, ParticipantConstants.currentParticipantNr, ampRiseList)
    freefield.play()

    time.sleep(len(ampRiseList))
    Sprecher_und_Procs.turnAllLedsOff

    inp = input("Continue?")
    while True:
        if( inp.lower() == "yes" ):
            break

        
# fix amp rise list for this py

