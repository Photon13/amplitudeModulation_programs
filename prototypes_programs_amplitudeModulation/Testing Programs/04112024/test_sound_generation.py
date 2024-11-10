import os
from pathlib import Path
import typing
from typing import List
import datetime
import random
import pandas as pd
from pandas import DataFrame
import json
import openpyxl
import numpy
from numpy import ndarray
import ast
import pywin32

import slab
import freefield
#from freefield import Speaker
#from freefield import Processors
import IPython




__all__ = ["Speaker", "Processors"]+["Participant", "GlobalVariables", "GlobalsTechnicalStuff" "Paths", "LabPaths", "Experiment", "HelpMethodsParticipant"]

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

#print(slab.__version__)
#python -m pip install SoundCard
slab.sound._in_notebook=False # Laptop

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

if __name__ == "__main__":

    #slab.set_default_samplerate(44100)
    #signal = slab.Sound.multitone_masker(duration=3.0, low_cutoff=50, high_cutoff=12000, bandwidth=1/9)
    #signal.spectrum() # P/f
    #signal.waveform(end=200) #A/t ; 8000=1 sec for default sample rate
    #signal.play()



    #slab.set_default_samplerate(GlobalsSound.sample_rate)
    #base_stimulus = slab.Sound.pinknoise(duration=1.0)
    #base_stimulus.level = 70
    #base_stimulus = base_stimulus.ramp(duration=0.005) # ramp: continuous increase/decrease (for onset/offset) in amplitude
    #base_stimulus=base_stimulus.am(frequency=17.3, depth=0.9)
    #base_stimulus.play()
    #base_stimulus.spectrum() # P/f
    #base_stimulus.waveform(end=0.005) #A/t
    #print(base_stimulus)
