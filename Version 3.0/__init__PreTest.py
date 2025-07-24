import freefield
from typing import List
import numpy as np
import time

import json

from Globals import Globals
from ProcsSprecherLeds import Procs, Sprecher, Leds
from Generator import Generator

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORGREEN  = "\033[0;32m"
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


class PreTest:

    @staticmethod
    def run_preTest():

        #===============================================#               
                                                        #                            
        participantNr = 0            # <--              #       # Mk:0,    Gl:1,   Tm:2,   Alx:3,   Blnc:4      
                                                        #
        preTest_trial = 3            # <--              #
                                                        #
        ampRiseRange = [0.15, 0.35]       # <--         #       # default: [0.15, 0.35]   #both inclusive
                                                        #             
        #===============================================#

        famsLMR = Globals.FAM_LIST
        [listFirstHalf, listSecondHalf] = Generator.generate_nrSeq_preTest(ampRiseRange)

        pathFile : str = f"data\\preTest\\listFirstHalf_listSecondHalf\\participant{participantNr}_preTest{preTest_trial}.txt" 
        with open(pathFile, "w") as f:
            json.dump([listFirstHalf, listSecondHalf], f)
   
        while True:
            inp = input( COLORRED + "Remember to start recording! " + COLORGREEN + "Start? [yes]: " + COLOREND )
            if( inp.lower() == "yes"):
                break
        ##
        for shiftList in [listFirstHalf, listSecondHalf]:
            Procs.initFF()
            speakers, leds = Procs.pickSpeakersAndLeds()

            Leds.turnTargetLedOn(leds, "left")
            emptyAmpRiseList = Generator.generateListOfZeros( len(shiftList) )

            Sprecher.writeToSpeaker( "left",   speakers, famsLMR, shiftList )
            Sprecher.writeToSpeaker( "middle", speakers, famsLMR, emptyAmpRiseList )
            Sprecher.writeToSpeaker( "right",  speakers, famsLMR, emptyAmpRiseList )
            freefield.play()
     
            time.sleep(len(listFirstHalf))

            while True:
                inp = input(COLORGREEN + "Continue? [yes]" + COLOREND)
                if( inp.lower() == "yes"):
                    break

        print( COLORGREEN + "PreTest done. " + COLOREND )
        Leds.turnAllLedsOff(leds)
        freefield.halt()

        print(COLORCYAN + "pre_AMP_RISE_LIST 1: " + COLORYELLOW + f"{listFirstHalf}"  + COLOREND)
        print(COLORCYAN + "pre_AMP_RISE_LIST 2: " + COLORYELLOW + f"{listSecondHalf}" + COLOREND)
        print(COLORRED + "Remember to increment trial number if another preTest is performed for the same participant! " + COLOREND )

    ####


#PreTest.run_preTest() #funzt
# 2min 56 sec