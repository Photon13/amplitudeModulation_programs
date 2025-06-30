from CommonHelpFunctions import CommonHelpFunctions

from pathlib import Path
import os
import numpy as np
from typing import List

import freefield


class Freifeld:

    COORDINATES_DICT = {
        "COORDINATES_SPEAKER_LEFT"   :  (-35, 0),
        "COORDINATES_SPEAKER_MIDDLE" :  (0, 0),
        "COORDINATES_SPEAKER_RIGHT"  :  (35, 0),
        "COORDINATES_LED_LEFT"       :  (0, -25),
        "COORDINATES_LED_MIDDLE"     :  (0, 0),
        "COORDINATES_LED_RIGHT"      :  (0, 25)
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
        speakerCoordinates = Freifeld.COORDINATES_DICT[f"COORDINATES_SPEAKER_{position.upper()}"]
        [speaker] = freefield.pick_speakers(speakerCoordinates) 
        freefield.write( f"channel{position.capitalize()}",    speaker.analog_channel,             speaker.analog_proc )
        freefield.write( f"fam{position.capitalize()}",        fam,                                ["RX81", "RX82"]    )
        freefield.write( f"nrSeq{position.capitalize()}",      np.array(nrSeq).astype('float32'),  speaker.analog_proc )
        freefield.write( "n_secs", len(nrSeq), ["RX81", "RX82"] )


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

    @staticmethod #spelling correct
    def turnLedOn(position : str) -> None:
        ledCoordinates = Freifeld.COORDINATES_DICT[f"COORDINATES_LED_{position.upper()}"]
        [led] = freefield.pick_speakers(ledCoordinates)
        freefield.write( f"bitmask{position.capitalize()}",  led.digital_channel, led.digital_proc)

    @staticmethod
    def turnTargetLedOn(target : str) -> None:
        if(target.lower() == "both"):
            Freifeld.turnLedOn("Left")
            Freifeld.turnLedOn("Right")
        else:
            Freifeld.turnLedOn(target)


    @staticmethod
    def turnAllLedsOff() -> None:
        positions = ["Left", "Middle", "Right"]
        for pos in positions:
            ledCoordinates = Freifeld.COORDINATES_DICT[f"COORDINATES_LED_{pos.upper()}"]
            [led] = freefield.pick_speakers(ledCoordinates)
            freefield.write( f"bitmask{pos.capitalize()}",  0, led.digital_proc)


