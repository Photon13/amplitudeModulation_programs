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
from Experiment import Experiment
from HelpMethodsParticipant import HelpMethodsParticipant

__all__ = ["Participant", "GlobalVariables","Paths", "Experiment", "HelpMethodsParticipant"]

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


if __name__ == "__main__":

    participant_nr = 700
    """
    """
    fAM_A, fAM_B, fAM_C, shift, n_subblocks, n_blocks = GlobalVariables.get_globalvariables()
    possibilties_speaker_identity_fAM_A, possibilties_speaker_identity_fAM_B, possibilties_speaker_identity_fAM_C, possibilities_target, possibilities_shift_position = GlobalVariables.get_possibilities_globalvariables()
    """
    """
    path_cwd = Paths.path_cwd_pc_maik
    #path_cwd = Paths.path_cwd_pc_lab
    """
    """
    path_json, path_mp3, path_wav = Paths.get_non_cwd_paths(path_cwd)
    """
    """
