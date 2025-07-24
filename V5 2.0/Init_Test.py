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

import time



class Init_Test:

    @staticmethod
    def demonstration():
        famsLMR = ParticipantConstants.get_famList(0)
        ampRiseRange = [0.3, 0.3]

        Sprecher_und_Procs.initFF()
        speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

        shiftList1 = Generator.generate_nrSeq_preTest(ampRiseRange)[0] 
        nullList = Generator.generateListOfZeros( len(shiftList1) )

        Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, nullList)  
        Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, nullList)
        Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, shiftList1)

        freefield.play()


    @staticmethod
    def testSpeakers():
        Sprecher_und_Procs.initFF()
        speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

        ampRise = 0.3
        famsLMR = ParticipantConstants.FAM_LIST_01234[0]

        # --Linker Sprecher mit Shifts-- :
        nullList = [0.0,0.0, 0.0,0.0,0.0,0.0, 0.0]
        shiftList = [0.0,0.0, ampRise,ampRise,ampRise,ampRise, 0.0,0.0] #zu Sicherheit sollten die ersten und letzten zwei Sekunden shiftfrei sein
        #BVR bekommt scheinbar keine Marker, wenn die trigger zu nah am Programmstart oder -ende gesendet werden

        Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, shiftList)  
        Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, nullList)
        Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, nullList)
        Sprecher_und_Procs.turnTargetLedOn(leds, "left")

        freefield.play()
        time.sleep(len(shiftList))
        Sprecher_und_Procs.turnAllLedsOff(leds)



        # --Mittlerer Sprecher mit Shifts-- :
        nullList = [0.0,0.0, 0.0,0.0,0.0,0.0, 0.0]
        shiftList = [0.0,0.0, ampRise,ampRise,ampRise,ampRise, 0.0,0.0] #zu Sicherheit sollten die ersten und letzten zwei Sekunden shiftfrei sein
        #BVR bekommt scheinbar keine Marker, wenn die trigger zu nah am Programmstart oder -ende gesendet werden

        Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, nullList)
        Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, shiftList)
        Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, nullList)
        Sprecher_und_Procs.turnTargetLedOn(leds, "middle")

        freefield.play()
        time.sleep(len(shiftList))
        Sprecher_und_Procs.turnAllLedsOff(leds)



        # --Rechter Sprecher mit Shifts-- :
        nullList = [0.0,0.0, 0.0,0.0,0.0,0.0, 0.0]
        shiftList = [0.0,0.0, ampRise,ampRise,ampRise,ampRise, 0.0,0.0] #zu Sicherheit sollten die ersten und letzten zwei Sekunden shiftfrei sein
        #BVR bekommt scheinbar keine Marker, wenn die trigger zu nah am Programmstart oder -ende gesendet werden

        Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, nullList)
        Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, nullList)
        Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, shiftList)
        Sprecher_und_Procs.turnTargetLedOn(leds, "right")

        freefield.play()
        time.sleep(len(shiftList))
        Sprecher_und_Procs.turnAllLedsOff(leds)



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

@staticmethod
def test_delay():
    ampRise = 2.3
    delayTime = 3

    shiftList = []

    shiftList.extend( [0.0]*7 )
    shiftList.append(ampRise)
    shiftList.extend( [0.0]*7 )
    shiftList.append(ampRise)
    shiftList.extend( [0.0]*7 )
    shiftList.append(ampRise)
    shiftList.extend( [0.0]*2 )

    nullList = Generator.generateListOfZeros( len(shiftList) )


    Sprecher_und_Procs.initFF()
    speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

    famsLMR = ParticipantConstants.FAM_LIST_01234[0]

    Sprecher_und_Procs.writeToSpeaker("left", speakers, famsLMR, shiftList)  
    Sprecher_und_Procs.writeToSpeaker("middle", speakers, famsLMR, shiftList)
    Sprecher_und_Procs.writeToSpeaker("right", speakers, famsLMR, shiftList)

    inp = input( "Start recording!" )
    time.sleep(delayTime)

    freefield.play()


#Init_Test.testSpeakers()
#Init_Test.run_testAllLeds(7)
#Init_Test.demonstration()

