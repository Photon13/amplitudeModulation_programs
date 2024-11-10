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

class Paths:
    path_cwd_pc_maik:str
    path_cwd_pc_lab: str

    path_cwd_pc_maik = "D:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\5_Bachelorarbeit\\5_Version_data_programs_etc"
    # CHANGE:
    path_cwd_pc_lab = " <...> \\Maik Kuerschner\\Studium\\Biologie Bachelor\\Bachelorarbeit\\5_Bachelorarbeit\\5_Version_data_programs_etc"
    
    def get_non_cwd_paths(path_cwd):
        path_json = Path(path_cwd) / "Participant data" / "Participant information" / "json"
        path_mp3 = Path(path_cwd) / "Sound_files" / "mp3"
        path_wav = Path(path_cwd) / "Sound_files" / "wav"
        return path_json, path_mp3, path_wav

class LabPaths:
    # CHANGE:
    path_experiment_jitter_rcx = " "  

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

class GlobalVariables:

    fAM_A: float
    fAM_B: float
    fAM_C: float
    shift: float

    n_subblocks: int
    n_blocks: int

    possibilities_speaker_identity_fAM_A: List[str]
    possibilities_speaker_identity_fAM_B: List[str]
    possibilities_speaker_identity_fAM_C: List[str]

    possibilities_target: List[str]
    possibilities_shift_position: [str]

    ###

    fAM_A = 5.0
    fAM_B = 7.3
    fAM_C = 13.7
    shift = 6.0

    n_subblocks = 1+30 # No shift, 30*shift
    n_blocks = 2+16 # Test single_speaker=target, Test both=target, 16*normal_blocks

    possibilties_speaker_identity_fAM_A = ["(fAM_A=fAM_left)", "(fAM_A=fAM_middle)", "(fAM_A=fAM_right)" ]
    possibilties_speaker_identity_fAM_B = ["(fAM_B=fAM_left)", "(fAM_B=fAM_middle)", "(fAM_B=fAM_right)" ]
    possibilties_speaker_identity_fAM_C = ["(fAM_C=fAM_left)", "(fAM_C=fAM_middle)", "(fAM_C=fAM_right)" ]

    possibilities_target = ["(left=target)", "(middle=target)", "(right=target)", "(both=target)"]
    possibilities_shift_position = ["(shift=left)", "(shift=middle)", "(shift=right)"]


    @staticmethod
    def get_globalvariables():
        fAM_A = GlobalVariables.fAM_A
        fAM_B = GlobalVariables.fAM_B
        fAM_C = GlobalVariables.fAM_C
        shift = GlobalVariables.shift
        n_subblocks = GlobalVariables.n_subblocks
        n_blocks = GlobalVariables.n_blocks
        return fAM_A, fAM_B, fAM_C, shift, n_subblocks, n_blocks
    
    @staticmethod
    def get_possibilities_globalvariables():
        possibilties_speaker_identity_fAM_A = GlobalVariables.possibilties_speaker_identity_fAM_A
        possibilties_speaker_identity_fAM_B = GlobalVariables.possibilties_speaker_identity_fAM_B
        possibilties_speaker_identity_fAM_C = GlobalVariables.possibilties_speaker_identity_fAM_C
        possibilities_target = GlobalVariables.possibilities_target
        possibilities_shift_position = GlobalVariables.possibilities_shift_position
        return possibilties_speaker_identity_fAM_A, possibilties_speaker_identity_fAM_B, possibilties_speaker_identity_fAM_C, possibilities_target, possibilities_shift_position 

#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

class GlobalsSound:
    sample_rate = 44100 # default = 44100 1/s
    # for default sample rate: 8000 samples = 1 s

    amplitude_max = 70 # default = 70 dB
    depth_am = 1.0 # 1.0 = 100% amplitude modulation -> from 0 dB to amplitude_max
    fading_duration = 0.005 # default = 0.005 s ; duration of fading-in/fading-out, i.e. ramp duration
    
    duration_shift_in_sec = 3.0
    duration_shift_in_samples = slab.Signal.in_samples(duration_shift_in_sec, samplerate)

    duration_subblock_in_sec = 4.0
    duration_subblock_in_samples = slab.Signal.in_samples()

    def get_globals_sound():
        sample_rate = GlobalsSound.sample_rate
        amplitude_max = GlobalsSound.amplitude_max
        depth_am = GlobalsSound.depth_am
        fading_duration = GlobalsSound.fading_duration
        duration_shift_in_sec = GlobalsSound.duration_shift_in_sec
        duration_shift_in_samples = GlobalsSound.duration_shift_in_samples
        duration_subblock_in_sec = GlobalsSound.duration_subblock_in_sec
        duration_subblock_in_samples = GlobalsSound.duration_subblock_in_samples
        return sample_rate, amplitude_max, depth_am, fading_duration, duration_shift_in_sec, duration_shift_in_samples, duration_subblock_in_sec, duration_subblock_in_samples


#__________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

class GlobalsAndPathsTechnicalStuff:
    def get_speaker_indices():
        index_left_speaker = int(8) # = [(-17.5), 0.0]
        index_middle_speaker = int(23) # = [0.0, 0.0]
        index_right_speaker = int(38) # = [(+17.5), 0.0]
        return index_left_speaker, index_middle_speaker, index_right_speaker 