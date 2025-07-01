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






###test:
from Paths import Paths
proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
             ['RX81', 'RX8', Paths.PATH_RCX],
             ['RX82', 'RX8', Paths.PATH_RCX]]

freefield.initialize('dome', device = proc_list)
#leds = leds = freefield.pick_speakers(Globals.LED_COORDINATES)

Led.turnOn_targetLed_forTimeIntervall("left", 1)
Led.turnOn_targetLed_forTimeIntervall("middle", 1)
Led.turnOn_targetLed_forTimeIntervall("right", 1)

#print(leds[0].digital_channel) #4
#print(leds[1].digital_channel) #8
#print(leds[2].digital_channel) #16

#[led] = freefield.pick_speakers(Globals.LED_COORDINATES[0])
#print(led.digital_channel)
#[led] = freefield.pick_speakers(Globals.LED_COORDINATES[1])
#print(led.digital_channel)
#[led] = freefield.pick_speakers(Globals.LED_COORDINATES[2])
#print(led.digital_channel)
