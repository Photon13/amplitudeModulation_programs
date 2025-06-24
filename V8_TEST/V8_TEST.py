import os
from pathlib import Path
import numpy as np
import freefield

class V8_TEST:

    @staticmethod
    def freefieldInit():
        PATH_RCX : Path = Path(os.getcwd()) /"data"/"rcx"/"V8_TEST.rcx"
        proc_list = [['RP2', 'RP2', PATH_RCX],
                    ['RX81', 'RX8', PATH_RCX],
                    ['RX82', 'RX8', PATH_RCX]]

        freefield.initialize('dome', device = proc_list)
    


    @staticmethod
    def getCoordinates( type, position):
        if( type.lower() == "speaker"):
            if( position.lower() == "left" ):
                return (-35, 0)
            elif( position.lower() == "middle" ):
                return (0, 0)
            elif( position.lower() == "right" ):
                return (35, 0)
            
        elif( type.lower() == "led"):
            if( position.lower() == "left" ):
                return (0, -25)
            elif( position.lower() == "middle" ):
                return (0, 0)
            elif( position.lower() == "right" ):
                return (0, 25)



    @staticmethod
    def try_float64_array_and_fam():
        V8_TEST.freefieldInit()

        x = 0.3
        nrSeqsDict = {
            "Left" :   np.array([0.0, x, 0.0, x, 0.0, x, 0.0, x, 0.0, x, 0.0, x, 0.0, x, 0.0, x, 0.0, x, 0.0, x]).astype('float64'),
            "Middle" : np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]).astype('float64'),
            "Right" :  np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]).astype('float64')
        }
        famsDict = {
            "Left"   : 33.1, 
            "Middle" : 44.1, 
            "Right"  : 55.1
        }

        for pos in ["Left", "Middle", "Right"]:
            [speaker] = freefield.pickSpeakers( [V8_TEST.getCoordinates( "speaker", f"{pos}")] )
            freefield.write( f"channel{pos}", speaker.analog_channel,     speaker.analog_proc )
            freefield.write( f"fam{pos}",     famsDict[f"{pos}"],        ["RX81", "RX82"]     )
            freefield.write( f"nrSeq{pos}",   nrSeqsDict[f"{pos}"],      speaker.analog_proc  )
            freefield.write( "n_secs",        len(nrSeqsDict[f"{pos}"]), ["RX81", "RX82"]     )

V8_TEST.try_float64_array_and_fam()