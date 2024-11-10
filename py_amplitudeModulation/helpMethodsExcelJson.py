import os
from pathlib import Path
import pandas as pd
import json
import typing
from typing import List
import datetime
import random
import ast

from globals import GlobalPaths

__all__ = ["GlobalPaths"]

class HelpMethodsExcelJson:

    @staticmethod   
    def assign_speaker_identity():
        poss_speaker_identity_A = [
            "(fAM_A=fAM_left)", 
            "(fAM_A=fAM_middle)", 
            "(fAM_A=fAM_right)" 
        ]
        poss_speaker_identity_B = [
            "(fAM_B=fAM_left)", 
            "(fAM_B=fAM_middle)", 
            "(fAM_B=fAM_right)" 
        ]
        poss_speaker_identity_C = [
            "(fAM_C=fAM_left)", 
            "(fAM_C=fAM_middle)", 
            "(fAM_C=fAM_right)" ]
        # numbers 1, 2 and 3 are positioned in random order
        i = random.sample( 
            [0,1,2], k = 3
            ) 
        speaker_identity = [ 
            poss_speaker_identity_A[i[0]],
            poss_speaker_identity_B[i[1]], 
            poss_speaker_identity_C[i[2]] 
        ]
        return speaker_identity

# '(fAM_left=fAM_A=5Hz)' '()' '()'






if __name__ == "__main__":
    
    participant_nr = 888

    path_cwd, path_json_excel, path_excel, path_json = GlobalPaths.getPaths()
    fAM_A, fAM_B, fAM_C, shift = GlobalPaths.getGlobalsSound()