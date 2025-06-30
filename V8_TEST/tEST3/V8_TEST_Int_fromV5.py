import os
from pathlib import Path
import numpy as np
import freefield

class V8_TEST_Int_fromV5:
    """uses int32 instead of float and chooses shift by a binary decision: nrSeq: 1 -> no shift, nrSeq: 2 -> shift"""

    def v8_TEST_Int_fromV5():

        PATH_RCX : Path = Path(os.getcwd()) / "V8_TEST_Int_fromV5.rcx"
        proc_list = [['RP2', 'RP2', PATH_RCX],
                    ['RX81', 'RX8', PATH_RCX],
                    ['RX82', 'RX8', PATH_RCX]]

        freefield.initialize('dome', device = proc_list)

        [speakerLeft] = freefield.pick_speakers( [-35, 0] )


        nrSeqLeft = []
        nrSeqLeft.extend([1]*5) #CAVE 1.0 is default
        nrSeqLeft.extend([2]*3) 
        nrSeqLeft.extend([1]*5) 
        nrSeqLeft = np.array(nrSeqLeft).astype('int32')

        famLeft = 33.0


        freefield.write( f"channelLeft", speakerLeft.analog_channel,     speakerLeft.analog_proc )
        freefield.write( f"famMiddle",   famLeft,                        ["RX81", "RX82"]     )
        freefield.write( f"nrSeqRight",  nrSeqLeft,                      speakerLeft.analog_proc  )
        freefield.write( "n_secs",       len(nrSeqLeft),                 ["RX81", "RX82"]     )
        freefield.write( "ampRise",      0.3,                            ["RX81", "RX82"]     )
        freefield.write( "volume",       0.18,                           ["RX81", "RX82"]     )


V8_TEST_Int_fromV5.v8_TEST_Int_fromV5()
    