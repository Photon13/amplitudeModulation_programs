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

class Init_tests:

    @staticmethod
    def run_testAllLeds():
        Sprecher_und_Procs.initFF()
        speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()
        time.sleep(10)

        for t in ["left", "middle", "right", "both"]:
            Sprecher_und_Procs.turnTargetLedOn(leds, t)
            time.sleep(1)
            Sprecher_und_Procs.turnAllLedsOff(leds)
            time.sleep(1)

#Init_tests.run_testAllLeds()