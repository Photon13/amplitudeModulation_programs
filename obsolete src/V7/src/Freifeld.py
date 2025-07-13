from CommonHelpFunctions import CommonHelpFunctions

from pathlib import Path
import os
import numpy as np
from typing import List

import freefield


class Freifeld:

    COORDINATES_DICT = {
        "speakerLeft"   :  (-35, 0),
        "speakerMiddle" :  (0, 0),
        "speakerRight"  :  (35, 0),
        "ledLeft"       :  (0, -25),
        "ledMiddle"     :  (0, 0),
        "ledRight"      :  (0, 25)
    }

    #PATH_RCX : Path = Path(os.getcwd()) /"data"/"rcx"/"V7_test.rcx"
    PATH_RCX : Path = Path(os.getcwd()) /"data"/"rcx"/"V7_fixShift.rcx"

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    def init_FF() -> None: #works
        proc_list = [['RP2', 'RP2', Freifeld.PATH_RCX],
                    ['RX81', 'RX8', Freifeld.PATH_RCX],
                    ['RX82', 'RX8', Freifeld.PATH_RCX]]

        freefield.initialize('dome', device = proc_list)

    #--------------------------------------------------------------------------------------------------------------------|

    @staticmethod
    def writeToSpeaker(position : str, fam : float, nrSeq : List[float]):
        pos    = position.capitalize() #new
        n_secs = len(nrSeq)       #new
        nrSeq  = np.array(nrSeq).astype('float32') #new: 32 bit

        speakerCoordinates = Freifeld.COORDINATES_DICT[f"speaker{pos}"]
        [speaker] = freefield.pick_speakers([speakerCoordinates])  #new: []

        freefield.write( f"channel{pos}", speaker.analog_channel, speaker.analog_proc ) #new: pos
        freefield.write( f"nrSeq{pos}",   nrSeq,                  speaker.analog_proc )
        freefield.write( f"fam{pos}",     fam,                    ["RX81", "RX82"]    )
        freefield.write( "n_secs",        n_secs,                 ["RX81", "RX82"]    )
        


    @staticmethod
    def writeToAllSpeakers(famsLMR : List[float], nrSeqsLMR : List[List]):
        positions : List[str] = ["Left", "Middle", "Right"]
        for i in range(3):
            Freifeld.writeToSpeaker( positions[i], famsLMR[i], nrSeqsLMR[i] )

    #--------------------------------------------------------------------------------------------------------------------|

    @staticmethod
    def sendTrigger_afterShortDelay() -> None:
        CommonHelpFunctions.waitForXSeconds(1)
        freefield.play()
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod
    def turnLedOn(position : str) -> None:
        pos = position.capitalize()
        ledCoordinates = Freifeld.COORDINATES_DICT[f"led{pos}"]
        [led] = freefield.pick_speakers( [ledCoordinates] )

        freefield.write( f"bitmask{pos}",  led.digital_channel, led.digital_proc)

    @staticmethod
    def turnTargetLedOn(target : str) -> None:
        if(target.lower() == "both"):
            Freifeld.turnLedOn("Left")
            Freifeld.turnLedOn("Right")
        else:
            Freifeld.turnLedOn(target)


    @staticmethod
    def turnAllLedsOff() -> None:
        for pos in ["Left", "Middle", "Right"]:
            ledCoordinates = Freifeld.COORDINATES_DICT[f"led{pos}"]
            [led] = freefield.pick_speakers( [ledCoordinates] )

            freefield.write( f"bitmask{pos}", 0, led.digital_proc)


