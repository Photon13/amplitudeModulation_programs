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

__all__ = ["Participant", "GlobalVariables", "Experiment", "HelpMethodsParticipant"]


#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

participant_nr: int

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

"""
1. change participant number 

2. change cwd paths:

    (if PC Maik used):
        enable:
            path_cwd_PC_Maik = r"D:\Maik\Studium\Biologie Bachelor\Bachelorarbeit\5_Bachelorarbeit\5_Version_data_programs_etc"
            path_cwd = path_cwd_PC_Maik
        disable ( -> #):
            path_cwd_PC_Lab = r" ... " 
            path_cwd = path_cwd_PC_Lab

    (if PC Lab used):
        disable ( -> #):
            path_cwd_PC_Maik = "..."
            path_cwd = Path(path_cwd_PC_Maik)
        enable:
            path_cwd_PC_Lab = " ... " -> 1st time: write path into string
            path_cwd = Path(path_cwd_PC_Lab)

"""

# CHANGE
path_cwd_PC_Maik = "D:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\5_Bachelorarbeit\\5_Version_data_programs_etc"
path_cwd = Path(path_cwd_PC_Maik)
#path_cwd_PC_Lab = " <...> \\Maik Kuerschner\\Studium\\Biologie Bachelor\\Bachelorarbeit\\5_Bachelorarbeit\\5_Version_data_programs_etc"
#path_cwd = Path(path_cwd_PC_Lab)

# KEEP 
path_json = Path(path_cwd) / "Participant data" / "Participant information" / "json"
path_mp3 = Path(path_cwd) / "Sound_files" / "mp3"
path_wav = Path(path_cwd) / "Sound_files" / "wav"


#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

class PreparationParticipantInformation:

    @staticmethod
    def generate_json_check_if_exists(participant_nr, fAM_A, fAM_B, fAM_C, shift, n_blocks, n_subblocks, path_json):
        """
        generate name
        """
        name = HelpMethodsParticipant.generate_name(participant_nr)

        """
        let user check whether GlobalVariables are set correctly
        """
        print(f"Participant Name is {name}.")
        print(f"fAM_A = {fAM_A} Hz, fAM_B = {fAM_B} Hz, fAM_C = {fAM_C} Hz, shift = {shift} Hz.")
        print(f"Number of blocks = 2+{n_blocks-2}, Number of subblocks = 1+{n_subblocks-1}.")

        while True:
            inp=input("Everything correct? Continue? yes/no:")
            if inp.lower() == "yes":
                break

        """
        check whether file exists or not
        """
         ##if file doesn't exists:
                #print("No file there yet. You may continue.")
        ##elif: file exists
            #print("File already exists! Check participant number")
        ##else:
            #print("Error occured in searching for preexisting json file")
            #break
        while True:
            inp=input ("Continue? yes/no: ")
            if inp.lower() == "yes":
                break
        """
        generate frequency assignment
        """
        xstr_frequencies = HelpMethodsParticipant.generate_xstr_frequencies(fAM_A, fAM_B, fAM_C, shift)
        """
        generate speaker identity assignment
        """
        xstr_speaker_identity = HelpMethodsParticipant.generate_xstr_speaker_identity(possibilties_speaker_identity_fAM_A, possibilties_speaker_identity_fAM_B, possibilties_speaker_identity_fAM_C)

        print(" ")

    
    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

#while True:
#    print(f"        Number of blocks is 2+{n_blocks-2}.")
#    print(f"        Number of subblocks is 1+{n_subblocks-1}.")
#    inp=input ("Continue with generating excel? yes/no: ")
#    if inp.lower() == "yes":
#        break
#HelpMethodsParticipant.generate_and_save_df_targets_and_shifts(participant_nr, n_blocks, n_subblocks, possibilities_target, possibilities_shift_position, path_json)
#print ("Excel file created successfully!")

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

if __name__ == "__main__":
    
    participant_nr = 700

    """
    1. import the global Variables of the experiment

    """
    fAM_A, fAM_B, fAM_C, shift, n_subblocks, n_blocks = GlobalVariables.get_globalvariables()
    possibilties_speaker_identity_fAM_A, possibilties_speaker_identity_fAM_B, possibilties_speaker_identity_fAM_C, possibilities_target, possibilities_shift_position = GlobalVariables.get_possibilities_globalvariables()
    
    """
    2. generate name, frequency assignment and speaker identity
    3. export name, frequency assignment and speaker identity to json
    4. export targets and shift occurrence to excel
    
    """
    name = HelpMethodsParticipant.generate_name(participant_nr)
    xstr_frequencies = HelpMethodsParticipant.generate_xstr_frequencies(fAM_A, fAM_B, fAM_C, shift)
    xstr_speaker_identity = HelpMethodsParticipant.generate_xstr_speaker_identity(possibilties_speaker_identity_fAM_A, possibilties_speaker_identity_fAM_B, possibilties_speaker_identity_fAM_C)
    
    PreparationParticipantInformation.export_json(name, xstr_frequencies, xstr_speaker_identity)

    HelpMethodsParticipant.generate_and_save_df_targets_and_shifts(participant_nr, n_blocks, n_subblocks, possibilities_shift_position, path_json)

    """
    REMEMBER TO PRE-GENERATE MP3s, if necessary !

    """

    
 