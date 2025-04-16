from Globals import Globals
from Sprecher import Sprecher

import freefield

import time

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'




class Led:

    @staticmethod
    def turnOn_targetLed(target :str):
        if( target == "both" ):
            positionen = ["left", "right"]
        else:
            positionen = [target]

        for position in positionen:
                led = Sprecher.get_coord(position, "led")
                freefield.write( f"bitmask{position.capitalize()}", led.digital_channel, led.digital_proc)



    @staticmethod
    def turnOff_allLeds():
        leds = freefield.pick_speakers( Globals.LED_COORDINATES)
        freefield.write( "bitmaskLeft", 0, leds[0].digital_proc)
        freefield.write( "bitmaskMiddle", 0, leds[1].digital_proc)
        freefield.write( "bitmaskRight", 0, leds[2].digital_proc)

        # AVH bits: 2,3,4 (-25,0),(0,0),(25,0)
        # freefield bits: 2,3,4 (-25,0),(0,0),(25,0)
        # freefield_dev bits: 2,3,4 (-25,0),(0,0),(25,0)



    @staticmethod
    def turnOn_targetLed_forTimeIntervall(target :str, n_subblocks : int):
        Led.turnOn_targetLed(target)

        duration : int = 4*n_subblocks
        ende = time.time() + duration
        while True:
            if( time.time()>= ende):
                Led.turnOff_allLeds()
                break



    




