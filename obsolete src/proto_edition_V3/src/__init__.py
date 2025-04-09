from Globals import Globals
from Paths import Paths
from Sequences import Sequences
from Participant import Participant

import freefield
import slab

from typing import List
from pathlib import Path
import numpy as np
import sys
import time
import random
import inspect



COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)




class Main:

    @staticmethod
    def get_coord(position : str, type :str):
        if( position == "left"):
            n : int = 0
        elif( position == "middle"):
            n : int = 1
        elif( position == "right"):
            n : int = 2
        else:
            print(COLORRED + "Invalid position!" + COLOREND + "get_coord()")

        if(type.lower() == ("speaker" or "speakers")):
            [speaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[n])
            return speaker
        elif(type.lower() == ("led" or "leds")):
            [led] = freefield.pick_speakers(Globals.LED_COORDINATES[n])
            return led

    @staticmethod
    def gen_shiftOccurrence(n_subblocks : int):
        shiftOccurrence : List[str] = ["none"]
        for i in range(1, n_subblocks):
            shiftOccurrence.append(random.choice(["left", "middle", "right"]))
        return shiftOccurrence
    
    @staticmethod
    def gen_shiftPossList():
        poss1 = [2, 1, 1, 1]        # should work, because Schmitt is open for 200 ms if 2 comes
        poss2 = [1, 2, 1, 1]        # but marker for shift start is sent immediately, when 2 comes
        poss3 = [1, 1, 2, 1]        # thus, participants have almost 1 sec until next shift might occur to press button
        poss4 = [2, 1, 2, 1]        
        poss5 = [1, 2, 2, 1]        # last sec always shift-less
        poss6 = [2, 2, 1, 1]
        return [poss1, poss2, poss3, poss4, poss5, poss6]

    @staticmethod
    def gen_nrSeq(position : str, shiftOccurrence : List[str]):
        shiftPossList = Main.gen_shiftPossList()
        nrSeq : List[int] = [1,1,1,1]
        for i in range(1, len(shiftOccurrence)):
            if(shiftOccurrence[i] == position):
                poss = random.choice(shiftPossList)
                for nr in poss:
                    nrSeq.append(nr)
            else:
                for nr in [1,1,1,1]:
                    nrSeq.append(nr)
        nrSeq = np.array(nrSeq).astype('int32')
        return nrSeq

    @staticmethod
    def gen_randomFamList() -> List[float]:
        return random.sample(Globals.FAM_LIST, k=3)


    @staticmethod
    def test_speakers(positionen : List[str], n_subblocks : int, famList : List[float]):
        shiftOccurrence = Main.gen_shiftOccurrence(n_subblocks)

        print(shiftOccurrence)
        famList : List[float] = Main.gen_randomFamList()

        for i in range(len(positionen)):
            position : str = positionen[i]
            speaker = Main.get_coord(position, "speaker")
            print(f"{position} {speaker.analog_proc}")
            freefield.write(f"channel{position.capitalize()}", speaker.analog_channel, speaker.analog_proc)
            nrSeq = Main.gen_nrSeq(position, shiftOccurrence)
            print(nrSeq)
            freefield.write(f"nrSeq{position.capitalize()}", nrSeq, speaker.analog_proc)
            freefield.write(f"fam{position.capitalize()}", famList[i], speaker.analog_proc)
            freefield.write("ampRise", 0.4, speaker.analog_proc)
            freefield.write("n_snippets", len(nrSeq), speaker.analog_proc)
            if(len(positionen) == 1):
                freefield.write("volumeFactor", 0.2, speaker.analog_proc)
            else:
                freefield.write("volumeFactor", 0.15, speaker.analog_proc) # if more than 1 speaker on, total volume will be higher -> single volumes should be reduced
        freefield.play()



    @staticmethod
    def test_singleSpeaker(position : str, n_subblocks : int, freq : float):
        positionen = [position]
        famList : List[float] = [freq]
        Main.test_speakers(positionen, n_subblocks, famList)

    @staticmethod
    def test_threeSpeakers(n_subblocks : int):
        positionen = ["left", "middle", "right"]
        Main.test_speakers(positionen, n_subblocks, Main.gen_randomFamList())

    @staticmethod
    def testLed(target :str, n_subblocks : int):
        duration : int = 4*n_subblocks

        if( target == "both" ):
            positionen = ["left", "right"]
        else:
            positionen = [target]

        for position in positionen:
                led = Main.get_coord(position, "led")
                freefield.write( f"bitmask{position.capitalize()}", led.digital_channel, led.digital_proc)

        ende = time.time() + duration
        while True:
            if( time.time()>= ende):
                Main.turnOff_allLeds()

    @staticmethod
    def turnOff_allLeds( ):
        leds = freefield.pick_speakers( Globals.LED_COORDINATES)
        freefield.write( "bitmaskLeft", 0, leds[0].digital_proc)
        freefield.write( "bitmaskMiddle", 0, leds[1].digital_proc)
        freefield.write( "bitmaskRight", 0, leds[2].digital_proc)

        # AVH bits: 2,3,4 (-25,0),(0,0),(25,0)
        # freefield bits: 2,3,4 (-25,0),(0,0),(25,0)
        # freefield_dev bits: 2,3,4 (-25,0),(0,0),(25,0)




    @staticmethod
    def test_speakers_modified_withBothProcs(positionen : List[str], n_subblocks : int):
        leftSpeaker = Main.get_coord("left", "speaker")
        rightSpeaker = Main.get_coord("right", "speaker")
        rx82 = leftSpeaker.analog_proc
        rx81 = rightSpeaker.analog_proc


        shiftOccurrence = Main.gen_shiftOccurrence(n_subblocks)

        print(shiftOccurrence)
        famList : List[float] = Main.gen_randomFamList()

        for i in range(len(positionen)):
            position : str = positionen[i]
            speaker = Main.get_coord(position, "speaker")
            print(f"{position} {speaker.analog_proc}")

            freefield.write(f"channel{position.capitalize()}", speaker.analog_channel, [rx81, rx82] )
            nrSeq = Main.gen_nrSeq(position, shiftOccurrence)
            print(nrSeq)

            freefield.write(f"nrSeq{position.capitalize()}", nrSeq, [rx81, rx82] )
            freefield.write(f"fam{position.capitalize()}", famList[i], [rx81, rx82] )
            freefield.write("ampRise", 0.4, [rx81, rx82] )
            freefield.write("n_snippets", len(nrSeq), [rx81, rx82] )

            if(len(positionen) == 1):
                freefield.write("volumeFactor", 0.2, [rx81, rx82] )
            else:
                freefield.write("volumeFactor", 0.15, [rx81, rx82] ) # if more than 1 speaker on, total volume will be higher -> single volumes should be reduced
        freefield.play()




if __name__ == "__main__":

    proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
                 ['RX81', 'RX8', Paths.PATH_RCX],
                 ['RX82', 'RX8', Paths.PATH_RCX]]
    
    freefield.initialize('dome', device=proc_list)

    n_subblocks = 8
    #Main.test_threeSpeakers(n_subblocks)
    Main.test_singleSpeaker("right", n_subblocks, 4.7)
    Main.testLed("both", n_subblocks)














