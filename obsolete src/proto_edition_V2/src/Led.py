from Globals import Globals

import freefield

import sys
import time

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'




class Led():

    @staticmethod 
    def turn_targetLed_on(target : str):
        """ target: either "left", "middle", "right" or "both" """

        [ledLeft] = freefield.pick_speakers( Globals.LED_COORDINATES[0])
        [ledMiddle] = freefield.pick_speakers( Globals.LED_COORDINATES[1])
        [ledRight] = freefield.pick_speakers( Globals.LED_COORDINATES[2])

        if( target == "left" ):
            freefield.write( "bitmaskLeft", ledLeft.digital_channel, ledLeft.digital_proc)

        elif( target == "middle" ):
            freefield.write( "bitmaskMiddle", ledMiddle.digital_channel, ledRight.digital_proc)

        elif( target == "right" ):
            freefield.write( "bitmaskRight", ledRight.digital_channel, ledRight.digital_proc)

        elif( target == "both" ):
            freefield.write( "bitmaskLeft", ledLeft.digital_channel, ledLeft.digital_proc)
            freefield.write( "bitmaskRight", ledRight.digital_channel, ledRight.digital_proc)

        else:
            print( COLORRED + "Invalid target in turn_targetLed_on" + COLOREND)
            sys.exit()
            
        print("    " + "TargetLed turned on. " + COLOREND)



    @staticmethod
    def turn_targetLed_onForIntervall(target : str, duration : int):
        Led.turn_targetLed_on(target)
        stoppZeit = time.time() + Globals.N_SUBBLOCKS*4
    
        while True:
            if time.time() > stoppZeit:
                Led.turn_all_leds_off()
            break
    
    
    
    @staticmethod
    def turn_all_leds_off( ):

        ledCoordinates  = Globals.LED_COORDINATES
        [ledLeft] = freefield.pick_speakers( ledCoordinates[0])
        [ledMiddle] = freefield.pick_speakers( ledCoordinates[1])
        [ledRight] = freefield.pick_speakers( ledCoordinates[2])

        freefield.write( "bitmaskLeft", 0, ledLeft.digital_proc)
        freefield.write( "bitmaskMiddle", 0, ledMiddle.digital_proc)
        freefield.write( "bitmaskRight", 0, ledRight.digital_proc)

        # AVH bits: 2,3,4 (-25,0),(0,0),(25,0)
        # freefield bits: 2,3,4 (-25,0),(0,0),(25,0)
        # freefield_dev bits: 2,3,4 (-25,0),(0,0),(25,0)