from Globals import Globals
from Sequences import Sequences

import freefield

from typing import List
import numpy as np


COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)


class Sprecher():

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
    def writeToAndTrigger_speakers(positionen : List[str], famList : List[float], shiftOccurrence : List[str]):

        for i in range(len(positionen)):
            position : str = positionen[i]
            speaker = Sprecher.get_coord(position, "speaker")

            freefield.write(f"channel{position.capitalize()}", speaker.analog_channel, ["RX81", "RX82"])
            
            nrSeq = Sequences.gen_nrSeq(position, shiftOccurrence)
            print(nrSeq)
            freefield.write(f"nrSeq{position.capitalize()}", nrSeq, ["RX81", "RX82"])
            
            freefield.write(f"fam{position.capitalize()}", famList[i], ["RX81", "RX82"])
            freefield.write("ampRise", 0.45, ["RX81", "RX82"])
            freefield.write("n_snippets", len(nrSeq), ["RX81", "RX82"])

            if(len(positionen) == 1):
                freefield.write("volumeFactor", 0.22, ["RX81", "RX82"])
            else:
                freefield.write("volumeFactor", 0.2, ["RX81", "RX82"]) # if more than 1 speaker on, total volume will be higher -> single volumes should be reduced
        freefield.play()



 
