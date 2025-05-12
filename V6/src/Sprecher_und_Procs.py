from Globals import Globals
from Paths import Paths

import freefield

from typing import List
import numpy as np



class Sprecher_und_Procs:
     
    @staticmethod
    def initFF() -> None:

        proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
                    ['RX81', 'RX8', Paths.PATH_RCX],
                    ['RX82', 'RX8', Paths.PATH_RCX]]

        freefield.initialize('dome', device = proc_list)
        # freefield.set_logger('DEBUG')

    @staticmethod
    def pickSpeakersAndLeds() -> dict:

        speakerLedDict : dict = {}
        speakerLedDict["speakers"] = {
            "speakerLeft" :   freefield.pick_speakers( Globals.SPEAKER_COORDINATES[0] ) [0],
            "speakerMiddle" : freefield.pick_speakers( Globals.SPEAKER_COORDINATES[1] ) [0],
            "speakerRight" :  freefield.pick_speakers( Globals.SPEAKER_COORDINATES[2] ) [0]
        }
        speakerLedDict["leds"] = {
            "ledLeft" :   freefield.pick_speakers( Globals.LED_COORDINATES[0] ) [0],
            "ledMiddle" : freefield.pick_speakers( Globals.LED_COORDINATES[1] ) [0],
            "ledRight" :  freefield.pick_speakers( Globals.LED_COORDINATES[2] ) [0]
        }
        return speakerLedDict
    


    @staticmethod
    def writeToSingleSpeaker(speakerLedDict : dict, position : str, fams : List[float], nrSeq : List[float]) -> None:

        speaker = speakerLedDict["speakers"][f"speaker{position.capitalize()}"]

        freefield.write(  "volume",            Globals.VOLUME,                    ["RX81", "RX82"] ) 
        freefield.write(  "n_snippets",        len(nrSeq),                        ["RX81", "RX82"] )
        freefield.write( f"fam{position}",     fams,                              ["RX81", "RX82"] )
        freefield.write( f"channel{position}", speaker.analog_channel,            speaker.analog_proc )
        freefield.write( f"nrSeq{position}",   np.array(nrSeq).astype('float64'), speaker.analog_proc )
        
        
        

    @staticmethod
    def writeToSpeakers_fromBlockDict(speakerLedDict : dict, blockDict : dict, blockNr : int) -> None:

        n_snippets = len( blockDict[f"block{blockNr}"]["nrSeqLeft"] )

        freefield.write( "n_snippets",   n_snippets,     ["RX81", "RX82"] )
        #freefield.write( "volume",       Globals.VOLUME, ["RX81", "RX82"] )

        positionen = ["Left", "Middle", "Right"]
        for pos in positionen:
            speaker =   speakerLedDict ["speakers"] [f"speaker{pos}"]
            fam =       blockDict      ["fams"]     [f"fam{pos}"]
            nrSeq =     blockDict      [f"block{blockNr}"] [f"nrSeq{pos}"]

            freefield.write( f"channel{pos}",    speaker.analog_channel,             speaker.analog_proc )
            freefield.write( f"fam{pos}",        fam,                                ["RX81", "RX82"] )
            freefield.write( f"nrSeq{pos}",      np.array(nrSeq).astype('float64'),  speaker.analog_proc )
        


    @staticmethod
    def turnTargetLedOn(speakerLedDict : dict, target : str) -> None:

        if( target == "both" ):
            led = speakerLedDict ["leds"] ["ledLeft"]
            freefield.write( f"bitmaskLeft",  led.digital_channel, led.digital_proc)

            led = speakerLedDict ["leds"] ["ledRight"]
            freefield.write( f"bitmaskRight", led.digital_channel, led.digital_proc)
        
        elif( target == ("left" or "middle" or "right") ):
            led = speakerLedDict ["leds"] [f"led{target.capitalize()}"]
            freefield.write( f"bitmask{target.capitalize()}", led.digital_channel, led.digital_proc)



    @staticmethod
    def turnAllLedsOff(speakerLedDict : dict) -> None:

        positionen = ["Left", "Middle", "Right"]
        for pos in positionen:
            freefield.write( "bitmaskLeft", 0, speakerLedDict["leds"][f"led{pos}"].digital_proc)






 
