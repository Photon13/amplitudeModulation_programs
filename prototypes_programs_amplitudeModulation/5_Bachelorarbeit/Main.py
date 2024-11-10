# import official modules/packages:
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

# import self-made classes:
from Participant import Participant
from GlobalVariables import GlobalVariables
from GlobalVariables import Paths
from GlobalVariables import GlobalsSound
from GlobalVariables import GlobalsAndPathsTechnicalStuff
from Experiment import Experiment
from HelpMethodsParticipant import HelpMethodsParticipant

__all__ = ["Participant", "GlobalVariables", "Paths", "GlobalsSound", "GlobalsAndPathsTechnicalStuff" "Experiment", "HelpMethodsParticipant"]


#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


if __name__ == "__main__":
   
    """
    0. import global stuff
        0.1 define participant number
            > > > > > PARTICIPANT NUMBER MUST BE SET MANUALLY !!!
        0.2 import global variables
        0.3 import paths
            > > > > > CHANGE PATH TO LAB OR MAIK depending on PC used !!!
    """
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
    path_rcx_circuit = GlobalsAndPathsTechnicalStuff.get_path_rcx_circuit(path_cwd)
    processor_list = GlobalsAndPathsTechnicalStuff.get_processor_list(path_rcx_circuit)
    """
    1. checks whether everythn works as desired
        1.1 check whether participant information (json and excel) exist
        1.2 check whether speakers and LEDs work
    
    """
    HelpMethodsParticipant.check_whether_participant_info_exists(participant_nr, path_json)
    """
    """
    HelpMethodsParticipant.check_whether_speakers_and_LEDs_work() # function not finished yet!
    """
    2. get name, frequency assignment and speaker identity from json (last two: as str and list)
    3. get targets and shift occurrence from excel

    """
    load_path_json = Path(json) / f"participant_{participant_nr}_df_targets_and_shifts.xlsx"
    name, xstr_frequencies, xstr_speaker_identity, xlist_frequencies, xlist_speaker_identity = HelpMethodsParticipant.load_json(participant_nr, path_json)
    """
    4. prepare detecting of start time for each block
        4.1 prepare list that shall contain start time blocks
        4.2 open df with targets and shifts and load into pd.DataFrame

    """
    start_times = ["start_times"] # str here as label for dataframe needed
    df_targets_and_shifts = HelpMethodsParticipant.load_df_targets_and_shifts(participant_nr, path_json) 
    """
    5. loop for playing respective block
        5.1 wait for input to start block
        5.2 defining block number
        5.3 append start time block to list
        5.4 create backup for start time as TEXT files

    """
    for i in range(n_blocks):
        
        while True:
            inp = input("Continue with next block? y: ")
            if inp.lower() == "y":
                break
        
        #get ... from list/df
        #search for block_name for block_nr

        block_nr = i
        HelpMethodsParticipant.add_start_times_to_list(block_nr, start_times)
        save_path_times_backup = Path(path_json) / "backup times" / f"{name}" f"backup_{name}_until_incl_block{block_nr}.txt"
        
        # read from df_targets_and_shifts
        #get target -> activate LED for block_nr
        #play mp3s for block_nr
    
    """
    6. save excel with times
    """
    HelpMethodsParticipant.save_start_times(start_times, participant_nr, n_blocks, path_json)

