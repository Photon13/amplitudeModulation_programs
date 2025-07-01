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


class Init_ampRise_anpassung:

    def init_ampRise_anpassung():

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


        ampRiseRange = [0.15, 0.4]
        listWithShifts = Generator.generate_nrSeq_preTest(ampRiseRange)
        emptyAmpRiseList = Generator.generateListOfZeros(len(listWithShifts))

        famsLMR = ParticipantConstants.FAM_LIST_01234[participantNr] ##
        print(famsLMR)
        


        Sprecher_und_Procs.initFF()
        speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

        Sprecher_und_Procs.turnTargetLedOn(leds, "middle") # PROBLEM?
        Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, listWithShifts)
        print(listWithShifts)
        Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, emptyAmpRiseList)
        Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, emptyAmpRiseList)

        freefield.play()


        time.sleep(len(listWithShifts))
        freefield.halt()
        print(Globals.COLORYELLOW + f"pre_AMP_RISE_LIST: {listWithShifts}" + Globals.COLOREND)






# blinking led on top?
# try shifts with ampRise between 0.1-0.3?
Init_ampRise_anpassung.init_ampRise_anpassung()
