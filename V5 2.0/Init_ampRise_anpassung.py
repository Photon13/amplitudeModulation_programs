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
        #===============================================#


        ampRiseRange = [0.1, 0.3]
        listWithShifts = Generator.generate_nrSeq_preTest(ampRiseRange)
        emptyAmpRiseList = Generator.generateListOfZeros(len(listWithShifts))


        famsLMR = ParticipantConstants.FAM_LIST_01234[participantNr] 

        ###
        
        while True:
            inp = input(Globals.COLORRED + "Remember to start recording! " + Globals.COLORCYAN + "Start? [yes]: " + Globals.COLOREND)
            if( inp.lower() == "yes"):
                break


        Sprecher_und_Procs.initFF()
        speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

        ##

        Sprecher_und_Procs.turnTargetLedOn(leds, "left")

        Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, listWithShifts)
        Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, emptyAmpRiseList)
        Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, emptyAmpRiseList)
        print(f"listWithshifts = {listWithShifts}")

        freefield.play()

        ##
        
        time.sleep(len(listWithShifts))
        Sprecher_und_Procs.turnAllLedsOff(leds)
        freefield.halt()
        
        print(Globals.COLORRED + "Copy pre_AMP_RISE_LIST into ParticipantConstants. " + Globals.COLOREND)
        print(Globals.COLORCYAN + "pre_AMP_RISE_LIST: " + Globals.COLORYELLOW + f"{listWithShifts}" + Globals.COLOREND)






# blinking led on top?
# try shifts with ampRise between 0.1-0.3?

Init_preTest.run_preTest()
