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

participantNr = ParticipantConstants.currentParticipantNr
#ampRiseList = ParticipantConstants.pre_AMP_RISE_LIST_01234[participantNr]
ampRiseList = Generator.gen_pre_AmpRiseList([0.10, 0.15, 0.2])
emptyAmpRiseList = Generator.gen_empty_AmpRiseList(len(ampRiseList))

Sprecher_und_Procs.initFF()
speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

Sprecher_und_Procs.turnTargetLedOn(leds, "middle") # PROBLEM?
Sprecher_und_Procs.writeToSpeaker("left", speakers, participantNr, ampRiseList)
Sprecher_und_Procs.writeToSpeaker("middle", speakers, participantNr, emptyAmpRiseList)
Sprecher_und_Procs.writeToSpeaker("right", speakers, participantNr, emptyAmpRiseList)

freefield.play()

time.sleep(len(ampRiseList))
Sprecher_und_Procs.turnAllLedsOff

inp = input("Continue?")
while True:
    if( inp.lower() == "yes" ):
        break



# blinking led on top?
# try shifts with ampRise between 0.1-0.3?
