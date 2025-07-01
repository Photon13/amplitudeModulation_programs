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

class Init_mainExp:

    participantNr = 0
    ampRise = ParticipantConstants.AMP_RISE_01234[participantNr]

    famsLMR = ParticipantConstants.FAM_LIST_01234[participantNr]



    Sprecher_und_Procs.initFF()
    speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()



    for i in range(Globals.N_BLOCKS):
        target =  ParticipantConstants.TARGET_LIST_01234[participantNr][i]
        Sprecher_und_Procs.turnTargetLedOn(leds, target)

        nrSeqList_left, nrSeqList_middle, nrSeqList_right = 
        Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, nrSeqList_left)

        Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, nrSeqList_middle)
        Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, nrSeqList_right)
        freefield.play()

        time.sleep(len(nrSeqList_left))
        Sprecher_und_Procs.turnAllLedsOff

        inp = input("Continue?")
        while True:
            if( inp.lower() == "yes" ):
                break

    freefield.halt()
            
    # fix amp rise list for this py