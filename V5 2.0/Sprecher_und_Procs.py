from Globals import Globals
from Sequences import Sequences
from Paths import Paths
from ParticipantConstants import ParticipantConstants

import freefield

from typing import List
import numpy as np



class Sprecher_und_Procs:
     
    @staticmethod
    def initFF():

        proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
                    ['RX81', 'RX8', Paths.PATH_RCX],
                    ['RX82', 'RX8', Paths.PATH_RCX]]

        freefield.initialize('dome', device = proc_list)


    @staticmethod
    def pickSpeakersAndLeds():

        [leftSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[0])
        [middleSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[1])
        [rightSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[2])
        speakers : List[freefield.Speaker] = [leftSpeaker, middleSpeaker, rightSpeaker] 

        [leftLed] = freefield.pick_speakers(Globals.LED_COORDINATES[0])
        [middleLed] = freefield.pick_speakers(Globals.LED_COORDINATES[1])
        [rightLed] = freefield.pick_speakers(Globals.LED_COORDINATES[2])
        leds : List[freefield.Speaker] = [leftLed, middleLed, rightLed]

        return speakers, leds
    

    @staticmethod #fixed 01.07.2025
    def writeToSpeaker(position : str, speakers : List[freefield.Speaker], famsLMR : List[float], ampRiseList : List[float]):
        if( position.lower() == "left"):
            i = 0
        elif( position.lower() == "middle"):
            i = 1
        elif( position.lower() == "right"): 
            i = 2          
        else:
            print(Globals.COLORRED + "Invalid position!" + Globals.COLOREND) ##

        position = position.capitalize() ##

        freefield.write(f"channel{position}", speakers[i].analog_channel, speakers[i].analog_proc)
        freefield.write("volume", Globals.VOLUME, ["RX81", "RX82"]) 
        freefield.write(f"fam{position}", famsLMR[i], ["RX81", "RX82"])
        
        freefield.write(f"nrSeq{position}", np.array(ampRiseList).astype('float64'), ["RX81", "RX82"])
        freefield.write("n_snippets", len(ampRiseList), ["RX81", "RX82"])
        

    
    @staticmethod
    def turnTargetLedOn(leds : List[freefield.Speaker], target):
        if(target == "both"):
            freefield.write( f"bitmaskLeft", leds[0].digital_channel, leds[0].digital_proc)
            freefield.write( f"bitmaskRight", leds[2].digital_channel, leds[2].digital_proc)
        
        elif(target == "left"):
            freefield.write( f"bitmaskLeft", leds[0].digital_channel, leds[0].digital_proc)
        elif(target == "middle"):
            freefield.write( f"bitmaskMiddle", leds[1].digital_channel, leds[1].digital_proc)
        else:
            freefield.write( f"bitmaskRight", leds[2].digital_channel, leds[2].digital_proc)


    @staticmethod
    def turnAllLedsOff(leds : List[freefield.Speaker]):
        freefield.write( "bitmaskLeft", 0, leds[0].digital_proc)
        freefield.write( "bitmaskMiddle", 0, leds[1].digital_proc)
        freefield.write( "bitmaskRight", 0, leds[2].digital_proc)
    





 
