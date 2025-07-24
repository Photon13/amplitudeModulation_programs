import freefield
from typing import List
import numpy as np
import time

from Globals import Globals
from Generator import Generator
from ProcsSprecherLeds import Procs, Sprecher, Leds

import time



class Init_Test:

    @staticmethod
    def demonstration():
        famsLMR = Globals.FAM_LIST
        ampRiseRange = [0.3, 0.3]

        Procs.initFF()
        speakers, leds = Procs.pickSpeakersAndLeds()

        shiftList1 = Generator.generate_nrSeq_preTest(ampRiseRange)[0] 
        nullList = Generator.generateListOfZeros( len(shiftList1) )

        Sprecher.writeToSpeaker("left", speakers, famsLMR, nullList)  
        Sprecher.writeToSpeaker("middle", speakers, famsLMR, nullList)
        Sprecher.writeToSpeaker("right", speakers, famsLMR, shiftList1)

        freefield.play()


    @staticmethod
    def testSpeakers():
        Procs.initFF()
        speakers, leds = Procs.pickSpeakersAndLeds()

        ampRise = 0.7
        famsLMR = Globals.FAM_LIST

        nullList = [0.0,0.0, 0.0,0.0,0.0,0.0, 0.0]
        shiftList = [0.0,0.0, ampRise,ampRise,ampRise,ampRise, 0.0,0.0] #zu Sicherheit sollten die ersten und letzten zwei Sekunden shiftfrei sein
        #BVR bekommt scheinbar keine Marker, wenn die trigger zu nah am Programmstart oder -ende gesendet werden

        # --Linker Sprecher mit Shifts-- :
        Sprecher.writeToSpeaker("left", speakers, famsLMR, shiftList)  
        Sprecher.writeToSpeaker("middle", speakers, famsLMR, nullList)
        Sprecher.writeToSpeaker("right", speakers, famsLMR, nullList)
        Leds.turnTargetLedOn(leds, "left")

        freefield.play()
        time.sleep(len(shiftList))
        Leds.turnAllLedsOff(leds)



        # --Mittlerer Sprecher mit Shifts-- :
        Sprecher.writeToSpeaker("left", speakers, famsLMR, nullList)
        Sprecher.writeToSpeaker("middle", speakers, famsLMR, shiftList)
        Sprecher.writeToSpeaker("right", speakers, famsLMR, nullList)
        Leds.turnTargetLedOn(leds, "middle")

        freefield.play()
        time.sleep(len(shiftList))
        Leds.turnAllLedsOff(leds)



        # --Rechter Sprecher mit Shifts-- :
        Sprecher.writeToSpeaker("left", speakers, famsLMR, nullList)
        Sprecher.writeToSpeaker("middle", speakers, famsLMR, nullList)
        Sprecher.writeToSpeaker("right", speakers, famsLMR, shiftList)
        Leds.turnTargetLedOn(leds, "right")

        freefield.play()
        time.sleep(len(shiftList))
        Leds.turnAllLedsOff(leds)



    @staticmethod
    def run_testAllLeds():
        Procs.initFF()
        speakers, leds = Procs.pickSpeakersAndLeds()
        time.sleep(10)

        for t in ["left", "middle", "right", "both"]:
            Leds.turnTargetLedOn(leds, t)
            time.sleep(1)
            Leds.turnAllLedsOff(leds)
            time.sleep(1)




Init_Test.testSpeakers() #funzt
#Init_Test.run_testAllLeds() #funzt
#Init_Test.demonstration() #funzt

# Shifts mittlerer Sprecher scheinen leiser zu sein, wenn man auf dem Stuhl sitzt
# aber wenn man das ohr direkt vor den jeweiligen Lautsprecher platziert, scheinen die shifts aller Lautsprecher gleich laut zu sein
