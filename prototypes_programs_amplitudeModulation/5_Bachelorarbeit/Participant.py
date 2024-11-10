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

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

class Participant:

    name: str # e.g. participant_1

    xlist_frequencies: List[str] # no attribute
    xstr_frequencies: str # e.g. "['(fAM_A=5.0Hz)', '(fAM_B=7.3Hz)', '(fAM_C=10.7Hz)', '(shift=6.0Hz)', 'shift_direction=increase']" ## increase/reduce
    
    xlist_speaker_identity: List[str] # no attribute
    xstr_speaker_identity: str # e.g. "['(fAM_A=fAM_left)', '(fAM_B=fAM_right)', '(fAM_C=fAM_middle)']""



    xlist_target_list: List[str] # no attribute
    xstr_target_list: str # e.g. "['(left=target)', '(both=target)', ... ]""
    
    df_subblocks_shift: pd.DataFrame # e.g. [{block0: ["(left=shift)", ("middle=shift"), ...]}, {block1: ["(right=shift)", ...]}, ...]

    list_time_block_start: List[str] # e.g. ['(14:28:31.450671)', '(14:30:31.450721)',...]
    xstr_time_block_start: str
    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    
    """
    initiate from given arguments

    """

    # initiation while data for t tests is collected, bevore initiation not needed
    def __init__(self, name, xstr_frequencies, xstr_target_list, xstr_speaker_identity, df_subblocks_shift, xstr_time_block_start):
        self.name = name # e.g. name = "participant_1"
        self.xstr_frequencies = xstr_frequencies
        self.xstr_speaker_identity = xstr_speaker_identity

        self.xstr_target_list = xstr_target_list
        self.df_subblocks_shift = df_subblocks_shift
        self.xstr_time_block_start = xstr_time_block_start
    
    """
    get values

    """

    def get_name(self):
        return self.name
    def get_xstr_frequencies(self):
        return self.xstr_frequencies
    def get_xstr_speaker_identity(self):
        return self.xstr_speaker_identity
    
    def get_xstr_target_list(self):
        return self.xstr_target_list
    def get_df_subblocks_shift(self):
        return self.df_subblocks_shift
    def get_xstr_time_block_start(self):
        return self.xstr_time_block_start

    """
        summarised method to call all getters 

    """

    def get_participant_information_without_times(self):
        self.get_name()
        self.get_xstr_frequencies()
        self.get_xstr_speaker_identity()

        self.get_xstr_target_list()
        self.get_df_subblocks_shift()
        self.get_xstr_time_block_start()

        return self.name, self.xstr_frequencies, self.xstr_speaker_identity, self.xstr_target_list, self.df_subblocks_shift 


