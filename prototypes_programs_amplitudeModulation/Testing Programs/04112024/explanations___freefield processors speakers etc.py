import pathlib
from pathlib import Path
import sys
__version__ = '0.1'
import numpy
import setuptools
import pandas
import matplotlib
#import pillow
import scipy
import insegel
#import ipython
import slab
#import opencv-python

sys.path.append('..\\')
DIR = pathlib.Path(__file__).parent.resolve()

import freefield
from freefield import PROCESSORS, DIR
from freefield.freefield import *


"""
# initialize()
# freefield.write() -> load sound into rcx buffer
# freefield.pick_speakers -> select speakers
# play()
"""
#____________________________________________________________________________________________________________________________________________________________________________
"""
proc_list : each sub-list represents one processor. 
            Contains name, model and circuit in that order

e.g.        <obj> = Processors()
            <obj>.initialize_processors (['RX81', 'RX8', 'example.rcx'],
                                        ['RX82', 'RX8', 'example.rcx'])
"""
"""
#proc_list = [['RX81', 'RX8', <path rcx file with circuit>)],
#             ['RX82', 'RX8', <path rcx file with circuit>]]
"""
#____________________________________________________________________________________________________________________________________________________________________________
""" 
freefield.pick_speakers(picks)  # picks = index or list of floats (degrees)
-> returns speakers
"""
"""
coordinates_left_speaker = [(-35.0), (0.0)] # Azimuth, Elevation
coordinates_right_speaker = [(+35.0), (0.0)]
# alternatives: 
#               [(-17.5), 0.0] and [(+17.5), 0.0]
#               [(-52.5), 0.0] and [(+52.5), 0.0]
"""
#____________________________________________________________________________________________________________________________________________________________________________
"""
freefield.initialize_setup("dome", default_mode="loctest_freefield", proc_list=None, zbus=True, connection="GB", camera_type=None)

# EITHER default_mode or proc_list must be given

#  if default_mode == "loctest_freefield":
#            proc_list = [['RP2', 'RP2',  DIR/'data'/'rcx'/'button.rcx'],
#                        ['RX81', 'RX8', DIR/'data'/'rcx'/'play_buf.rcx'],
#                         ['RX82', 'RX8', DIR/'data'/'rcx'/'play_buf.rcx']] is loaded AUTOMATICALLY
#
# conneciton 'GB': Glasfaser
"""

#____________________________________________________________________________________________________________________________________________________________________________
"""
# freefield.write(<channel name>, <speaker nr>, <proc_list>)
freefield.write(tag, value, procs) # = PROCESSORS.write(tag=tag, value=value, procs=procs)
"""

#____________________________________________________________________________________________________________________________________________________________________________
"""
freefield.play(kind='zBusA', proc=None) # = PROCESSORS.trigger(kind=kind, proc=proc)
"""
"""
freefield.play_and_wait()  # = PROCESSORS.trigger() + wait_to_finish_playing()
"""
"""
freefield.wait_to_finish_playing(proc="all", tag="playback")
"""

#____________________________________________________________________________________________________________________________________________________________________________
"""
freefield.set_signal_and_speaker(signal, speaker, equalize=True)


    Load a signal into the processor buffer and set the output channel to match the speaker.
    The processor is chosen automatically depending on the speaker.

        Args:
            signal (array-like): signal to load to the buffer, must be one-dimensional
            speaker (Speaker, int) : speaker to play the signal from, can be index number or [azimuth, elevation]
            equalize (bool): if True (=default) apply loudspeaker equalization

"""

#____________________________________________________________________________________________________________________________________________________________________________
"""
set_signal_and_speaker(signal, speaker, equalize=True)
"""

#____________________________________________________________________________________________________________________________________________________________________________

if __name__ =="__main__":

    #all([s.digital_channel for s in speakers])

    """
    left speaker = 8
    middle speaker = 23
    right speaker = 38
    """
    #path_cwd_tests_pc_lab = " <...> \\Maik Kuerschner\\Studium\\Biologie Bachelor\\Bachelorarbeit\\Testing programs"
    path_circuit_button_rcx = Path.cwd() / "rcx" / "button.rcx"
    path_circuit_play_buf_rcx = Path.cwd() / "rcx" / "play_buf.rcx"

    freefield.initialize_setup("dome", default_mode="loctest_freefield", proc_list=None, zbus=True, connection="GB", camera_type=None)
    # or             proc_list = [['RP2', 'RP2',  DIR/'data'/'rcx'/'button.rcx'],
    #                     ['RX81', 'RX8', DIR/'data'/'rcx'/'play_buf.rcx'],
    #                     ['RX82', 'RX8', DIR/'data'/'rcx'/'play_buf.rcx']]
    # my_proc.initialize(proc_list=proc_list, connection="GB")

    """ 
    if generation of sound during runtime 
    """

    Xsound = slab.Sound.pinknoise(duration=30.0) # duration in sec
    Xsound.level = 70
    Xsound = Xsound.ramp(duration=0.005)
    Xsound = Xsound.am(frequency=17.3, depth=0.9)
    
    freefield.write(tag="playbuflen", value=Xsound.n_samples, procs=["RX81", "RX82"]) # lenght in samples
    freefield.play_and_wait()


    """ 
    if wav used 
    """
    test_speaker = freefield.pick_speakers(8) # left one
    #path_Ysound = Path.cwd() / "test sounds"
    #Ysound = slab.Sound.read(path_Ysound)
    Ysound = []
    freefield.set_signal_and_speaker(signal=Ysound, speaker=test_speaker) #signal (Ysound) is one-dimensional array
    freefield.play_and_wait()


