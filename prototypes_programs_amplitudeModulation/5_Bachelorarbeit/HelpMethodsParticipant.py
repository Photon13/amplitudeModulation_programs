"""
Methods for preparation and saving data of participant:
    assignment speakers to fAMs
    assignment of targets to blocks
    assignments of shift position to subblocks

Methods for detecting and saving time of start for each blocks

Speaker identity will be saved as JSON. # preparated
Targets and shifts will be saved as an EXCEL table. # (without times) preparated
Times will be saved as TEXT for backup. # generated during experiment
Targets, shifts and times will be saved as an EXCEL table. # (with times) generated after experiment



Output example:

JSON:
    {
        "participant_700": {
            "name": "participant_700",
            "xstr_frequencies": "['(fAM_A=5.0Hz)', '(fAM_B=7.3Hz)', '(fAM_C=13.7Hz)', '(shift=6.0Hz)']",
            "xstr_speaker_identity": "['(fAM_A=fAM_left)', '(fAM_B=fAM_right)', '(fAM_C=fAM_middle)']"
        }
    }



EXCEL without times:
    (   blocks:         block0              block1              ...
        targets:        (left=target)       (both=target)       ...
        subblock0:      (right=shift)       (middle=shift)      ...
        subblock1:      (middle=shift)      (middle=shit)       ...
        subblock2:      (left=shift)        (right=shift)       ...
        ...             ...                 ...
    )

EXCEL with times:
    (   blocks:         block0              block1              ...
        targets:        (left=target)       (both=target)       ...
        subblock0:      (right=shift)       (middle=shift)      ...
        subblock1:      (middle=shift)      (middle=shit)       ...
        subblock2:      (left=shift)        (right=shift)       ...
        ...             ...                 ...
        start_block:    (18:47:23.345678)   (18:50:47.987654)   ...
    )

"""

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
from Experiment import Experiment

__all__ = ["Participant", "GlobalVariables", "Experiment"]







#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

class HelpMethodsParticipant:

    name: str # e.g. participant_1

    xlist_frequencies: List[str] 
    xstr_frequencies: str # e.g. "['(fAM_A=5.0Hz)', '(fAM_B=7.3Hz)', '(fAM_C=10.7Hz)', '(shift=6.0Hz)', 'shift_direction=increase']" ## increase/reduce

    xlist_speaker_identity: List[str] 
    xstr_speaker_identity: str # e.g. "['(fAM_A=fAM_left)', '(fAM_B=fAM_right)', '(fAM_C=fAM_middle)']""

    xlist_target_list: List[str] 
    xstr_target_list: str # e.g. "['(left=target)', '(both=target)', ... ]""
    
    df_subblocks_shift: pd.DataFrame # e.g. [{block0: ["(left=shift)", ("middle=shift"), ...]}, {block1: ["(right=shift)", ...]}, ...]

    list_time_block_start: List[str] # e.g. ['(14:28:31.450671)', '(14:30:31.450721)',...]
    xstr_time_block_start: str

    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    
    """
    write name based on participant number
    write frequencies  
    assign speakers to fAM_a, fAM_B and fAM_C
    
    """
    @staticmethod
    def generate_name(participant_nr):
        name = f"participant_{participant_nr}"
        return name
    
    @staticmethod
    def generate_xstr_frequencies(fAM_A, fAM_B, fAM_C, shift):
        xlist_frequencies = [f"(fAM_A={fAM_A}Hz)", f"(fAM_B={fAM_B}Hz)", f"(fAM_C={fAM_C}Hz)", f"(shift={shift}Hz)" ]
        xstr_frequencies = str(xlist_frequencies)
        return xstr_frequencies
    
    @staticmethod
    def generate_xstr_speaker_identity(possibilties_speaker_identity_fAM_A, possibilties_speaker_identity_fAM_B, possibilties_speaker_identity_fAM_C):
        i: List [int]
        i = random.sample ([0,1,2], k=3)
        xlist_speaker_identity = [possibilties_speaker_identity_fAM_A[i[0]], possibilties_speaker_identity_fAM_B[i[1]], possibilties_speaker_identity_fAM_C[i[2]]]
        xstr_speaker_identity = str(xlist_speaker_identity) 
        return xstr_speaker_identity
    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    
    """
    export name, frequencies and speaker identity as JSON

    """
    @staticmethod
    def export_json(participant_nr, name, xstr_frequencies, xstr_speaker_identity, path_json):
        save_path = Path(path_json) / f"participant_{participant_nr}_freq_speakeridentity.json" # name e.g. participant_1 
        dict= {
            f"{name}": {
                "name": name,
                "xstr_frequencies": xstr_frequencies,
                "xstr_speaker_identity": xstr_speaker_identity 
            }
        }

        file = open(save_path, "w")
        json.dump(dict, file) # .dump() converts data (here dict) into json format
        file.close()
        print ("'''''\n JSON file created sucessfully! \n'''''")
    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    
    """
    assign target per block
    assign shift per subblock
    and export assignments as EXCEL table
    
    """
    @staticmethod
    def generate_and_save_df_targets_and_shifts(participant_nr, n_blocks, n_subblocks, possibilities_shift_position, path_json):
        """ 
        prepare randomised target list, incl. training blocks (block0, block1)
            block0: training block for single speaker (left XOR right XOR middle)
            block1: training block for both 
        """
        targ_block0 = str(random.choice (["(left=target)", "(middle=target)", "(right=target)"])) 
        targ_block1 = str("(both=target)") 
        """
        normal blocks: each condition shall occur 4 times, order shall be random
        """
        n_trials_per_condition = int((1.0/4.0)*(n_blocks-2)) # for 2+16 blocks -> n_trials is 4, respectively
        help_list = n_trials_per_condition*["(left=target)"] + n_trials_per_condition*["(middle=target)"] + n_trials_per_condition*["(right=target)"] + n_trials_per_condition*["(both=target)"] # 4*(left=target) + 4*(middle=target) + 4*(right=target) + 4*(both=target)
        random.shuffle(help_list)
        """
        concatenate training blocks with normal blocks to list
        """
        xlist_target_list = [f"{targ_block0}"]
        xlist_target_list.append(targ_block1)
        xlist_target_list.extend(help_list) # EXTEND -> append only works for adding single String, but not for list[str]


        """
        prepare dataframe
        """
        column_names = ["subblock"] + [f"block{i}" for i in range(n_blocks)] #0st=header already given! n_blocks = 18 -> i.e. last block is block17 !
        n_rows = n_subblocks # last subblock=subblock31
        data = []
        targets = ["target"] + xlist_target_list # 1st row targets
        data.append(targets) 

        no_list = n_blocks*["(shift=NO)"]
        """
        subblock0 no shift
        """
        subblock0 = ["subblock0"] + no_list
        data.append(subblock0)
        """
        for each subblock create randomised shift occurrence position
        """
        for m in range(n_rows-2): 

            subblock_label = f"subblock{m}"
            block_targets = [random.choice(possibilities_shift_position) for _ in range (n_blocks)] # 0st = label (subblock) !
            row = [subblock_label] + block_targets
            data.append(row)

        """
        convert 'data' into pd.DataFrame
        and export pd.DataFrame as excel file
        """
        # data contains multiple lists: [[' ', ' ', ...], [' ', ' ', ...], [' ', ...], ...]
        # pd.DataFrame takes each of these "sublists" and puts them into a new row, respectively
        df_targets_and_shifts = pd.DataFrame(data, columns=column_names)
        save_path = Path(path_json) / f"participant_{participant_nr}_df_targets_and_shifts.xlsx"
        df_targets_and_shifts.to_excel(save_path, index=False)
        print("'''''\n Excel file created successfully! \n'''''")

    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    """
    checks

    """
    @staticmethod
    def check_whether_participant_info_exists(participant_nr, path_json):
        json_path = Path(path_json) / f"participant_{participant_nr}_freq_speakeridentity.json"
        excel_path = Path(path_json) / f"participant_{participant_nr}_df_targets_and_shifts.xlsx"
        #print (" ''''' ")
        if json_path.is_file(): #json exists
            if excel_path.is_file(): #excel exists
                print("'''''\n Participant Information (JSON and EXCEL) available. \n'''''")
            else: #excel doesn't exist
                print ("'''''\n CAVE: Participant Information (EXCEL) not available. \n'''''") 

        else: #json doesn't exist
            if excel_path.is_file(): #excel exists
                print("'''''\n CAVE: Participant Information (JSON) not available. \n'''''")
            else: #excel doesn't exist
                print("'''''\n CAVE: Participant Information (JSON and EXCEL) not available. \n'''''") 
        #print(" ''''' ")
    
    @staticmethod
    def check_whether_speakers_and_LEDs_work():
        while True:
            inp1 = input("Test speakers and LEDs now? yes/no: ")
            if inp1.lower() == "yes":
                #activate LEDs and play
                #5sec per target
                inp2 = input("Stop Testing? press any key to stop: ") # continues if something is entered
                break 
            elif inp1.lower() == "no":
                break
            #else: -> False -> repeat loop


    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    """
    loading JSON
    
    loading EXCEL

    """
    @staticmethod
    def load_json(participant_nr, path_json):
        load_path= Path(path_json) / f"participant_{participant_nr}_freq_speakeridentity.json"

        file = open(load_path, 'r')
        data = json.load(file)
        file.close()

        # Accessing the main dictionary for the participant
        participant_data = data['participant_700']

        # Extracting individual attributes
        name = participant_data['name']
        xstr_frequencies = participant_data['xstr_frequencies']
        xstr_speaker_identity = participant_data['xstr_speaker_identity']

        xlist_frequencies = ast.literal_eval(xstr_frequencies)
        xlist_speaker_identity = ast.literal_eval(xstr_speaker_identity)
        return name, xstr_frequencies, xstr_speaker_identity, xlist_frequencies, xlist_speaker_identity     


    @staticmethod
    def load_df_targets_and_shifts(participant_nr, path_json):
        load_path = Path(path_json) / f"participant_{participant_nr}_df_targets_and_shifts.xlsx"
        df_targets_and_shifts = pd.read_excel(load_path)
        return df_targets_and_shifts
    
    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    
    """
    get respective time start of a block
    append it to list of start times
    (loop in main needed!)

    add list to EXCEL table (as last row)
    save as new EXCEL file
    """

    @staticmethod
    def add_start_times_to_list(block_nr, start_times):
        next_time_entry = datetime.datetime.now()
        next_time_entry = next_time_entry.strftime("(%H:%M:%S.%f)")
        start_times.append(next_time_entry)
        print (f"Start time block {block_nr} appended to list.")
        return start_times

    @staticmethod
    def save_start_times(start_times, participant_nr, n_blocks, path_json):
        column_names = ["subblock"] + [f"block{i}" for i in range(n_blocks)]
        load_path = Path(path_json) / f"participant_{participant_nr}_df_targets_and_shifts.xlsx"
        load_path = str(load_path)
        xdf_targets_and_shifts = pd.read_excel(load_path) # CAVE .read_excel only takes String as path
        data = xdf_targets_and_shifts.values.tolist() #pd.DataFrame -> list of lists
        data.append(start_times) # adds start_times as new list (which shall be next row later)

        df_times_targets_shifts = pd.DataFrame(data, columns=column_names)
        print(df_times_targets_shifts)
        save_path = Path(path_json) / f"participant_{participant_nr}_df_times_targets_shifts.xlsx"
        df_times_targets_shifts.to_excel(save_path, index=False)
        print("'''''\n Excel file with times created successfully! \n'''''")

    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
   