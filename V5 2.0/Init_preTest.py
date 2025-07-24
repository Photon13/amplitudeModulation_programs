import freefield
from typing import List
import numpy as np
import time

import os
from pathlib import Path
import json
import re

from Globals import Globals
from Paths import Paths
from Sequences import Sequences
from Sprecher_und_Procs import Sprecher_und_Procs
from ParticipantConstants import ParticipantConstants
from Generator import Generator



class Init_preTest:

    @staticmethod
    def run_preTest():

        #===============================================#               
                                                        #                            
        participantNr = 0                               #               
        #Mk:   0                                        #
        #Gl:   1                                        #
        #Tm:   2                                        #
        #Alx:  3                                        #
        #Blnc: 4                                        #
                                                        #
        preTest_trial = 2                               #
                                                        #
        ampRiseRange = [0.15, 0.35]                     #       #default: [0.1, 0.3]   #both inclusive
                                                        #             
        #===============================================#


        famsLMR = ParticipantConstants.get_famList(participantNr)
        [listWithShifts1, listWithShifts2] = Generator.generate_nrSeq_preTest(ampRiseRange)

        cwd = os.getcwd()
        cwd_mod = cwd.replace("V5 2.0", "Data Analysis 2.0\\button press files")
        pathFile : Path = f"{cwd_mod}\\participant{participantNr}\\participant{participantNr}_preTest{preTest_trial}.txt" 
        with open(pathFile, "a") as f:
            json.dump([listWithShifts1, listWithShifts2], f)

        ##
        
        while True:
            inp = input(Globals.COLORRED + "Remember to start recording! " + Globals.COLORCYAN + "Start? [yes]: " + Globals.COLOREND)
            if( inp.lower() == "yes"):
                break
        ##

        for shiftList in [listWithShifts1, listWithShifts2]:
            Sprecher_und_Procs.initFF()
            speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

            Sprecher_und_Procs.turnTargetLedOn(leds, "left")
            emptyAmpRiseList = Generator.generateListOfZeros( len(shiftList) )

            Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, shiftList)
            Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, emptyAmpRiseList)
            Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, emptyAmpRiseList)
            print(f"listWithshifts = {listWithShifts1}")
            freefield.play()
     
            time.sleep(len(listWithShifts1))

            while True:
                inp = input("Continue? [yes]")
                if( inp.lower() == "yes"):
                    break

        print( Globals.COLORGREEN + "PreTest done. " + Globals.COLOREND )
        Sprecher_und_Procs.turnAllLedsOff(leds)
        freefield.halt()

        print(Globals.COLORCYAN + "pre_AMP_RISE_LIST 1: " + Globals.COLORYELLOW + f"{listWithShifts1}" + Globals.COLOREND)
        print(Globals.COLORCYAN + "pre_AMP_RISE_LIST 2: " + Globals.COLORYELLOW + f"{listWithShifts2}" + Globals.COLOREND)
        print(Globals.COLORRED + "Remember to increment trial number if another preTest is performed for the same participant! " + Globals.COLOREND )

    ####



#Init_preTest.run_preTest()
