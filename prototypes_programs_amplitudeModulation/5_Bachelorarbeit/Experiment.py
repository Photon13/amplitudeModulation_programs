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
import slab
#import freefield
import IPython

from Participant import Participant
from GlobalVariables import GlobalVariables
from GlobalVariables import Paths

__all__ = ["Participant", "GlobalVariables", "Experiment"]

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

class Experiment:

    """
    for Preparation_Main:
    
    """

    
    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

    """
    for Main:
    
    """
  
    
    @staticmethod        
    def check_EEG_active():
        print ("You can now activate the EEG Recording.")
        while True:
            confirmation = input ("    BrainVision Recorder activated? yes/no: ")
            if confirmation.lower == "yes":
                break

    @staticmethod        
    def test_keypress_events():
        while True:
            print ("Advise participant to press 'key 2' five times .")
            confirmation = input ("     Are key press events shown in BrainVision Recorder? yes/no: ")
            if confirmation.lower == "yes":
                break

    #@staticmethod
    #def play_blocks(n_blocks):
        # play block 0
        # play block 1
        #for i in range(2, n_blocks):

    


    