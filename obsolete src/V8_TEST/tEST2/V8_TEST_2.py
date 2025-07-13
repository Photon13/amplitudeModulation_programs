import os
from pathlib import Path
import numpy as np
import freefield

class V8_TEST_2:
    """ uses float32 and modified/simplified rcx construction"""

        
    def v8_TEST_2(): 

        PATH_RCX : Path = Path(os.getcwd()) / "V8_TEST_2.rcx"
        proc_list = [['RP2', 'RP2', PATH_RCX],
                    ['RX81', 'RX8', PATH_RCX],
                    ['RX82', 'RX8', PATH_RCX]]

        freefield.initialize('dome', device = proc_list)

        [speakerLeft] = freefield.pick_speakers( [-35, 0] )


        nrSeqLeft = []
        nrSeqLeft.extend([1.0]*5) #CAVE 1.0 is default
        nrSeqLeft.extend([1.3]*3) 
        nrSeqLeft.extend([1.0]*5) 
        nrSeqLeft = np.array(nrSeqLeft).astype('float32')

        famLeft = 33.0


        freefield.write( f"channelLeft", speakerLeft.analog_channel,     speakerLeft.analog_proc )
        freefield.write( f"famMiddle",   famLeft,                        ["RX81", "RX82"]     )
        freefield.write( f"nrSeqRight",  nrSeqLeft,                      speakerLeft.analog_proc  )
        freefield.write( "n_secs",       len(nrSeqLeft),                 ["RX81", "RX82"]     )


V8_TEST_2.v8_TEST_2()