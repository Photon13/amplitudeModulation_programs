import freefield

from Globals import Globals

__all__ = ["Globals"]

class Leds:
    
    def turn_targetLed_on( target ):

        ledCoordinates  = Globals.ledCoordinates
        ledLeft = freefield.pick_speakers( ledCoordinates[0])
        ledMiddle = freefield.pick_speakers( ledCoordinates[1])
        ledRight = freefield.pick_speakers( ledCoordinates[2])

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
            print( "Turning on target LED failed. Invalid target.")


    def turn_all_leds_off( ):

        ledCoordinates  = Globals.ledCoordinates
        ledLeft = freefield.pick_speakers( ledCoordinates[0])
        ledMiddle = freefield.pick_speakers( ledCoordinates[1])
        ledRight = freefield.pick_speakers( ledCoordinates[2])

        freefield.write( "bitmaskLeft", 0, ledLeft.digital_proc)
        freefield.write( "bitmaskMiddle", 0, ledRight.digital_proc)
        freefield.write( "bitmaskRight", 0, ledRight.digital_proc)

