from pathlib import Path
import pandas as pd
from datetime import datetime
import openpyxl 
import json

from Globals import Globals
from Participant import Participant

class ExportMethods:
    
    ### methods to add: EXPORT PARTICIPANT AS JSON (Block instances should already be included in Participant instance (?)) 
     


    """ creates empty list """
    @staticmethod
    def precreate_shiftOccurenceDf():
        protoDf_list = []
        return protoDf_list
    
    @staticmethod
    def append_shiftOccurence_toDf(shiftOccurence, protoDf_list, block_nr):
        new_data = [f"block_{block_nr}"] + shiftOccurence
        protoDf_list.append(new_data)
        return protoDf_list
    
    @staticmethod
    def generate_dfShiftOccurence(protoDf_list, participant_nr):
        date = datetime.today().strftime('%Y%m%d')

        save_path = Globals.path_cwd / f"participant{participant_nr}_{date}_ShiftOccurence.xlsx"

        columns = ["block"]
        for i in range (Globals.n_subblocks):
            columns.append(f"subblock_{i}")

        dfShiftOccurence = pd.DataFrame(data=protoDf_list, columns=columns)
        print( dfShiftOccurence)
        dfShiftOccurence.to_excel(save_path, index=False)
        








""" TEST:
participant_nr = 777
protoDf_list  = ExportMethods.precreate_shiftOccurenceDf()
shiftOccurence, nrSeqLeft, nrSeqMiddle, nrSeqRight = ShiftOccurenceSequenceMethods.generate_soundSequences()

for i in range (7):
    block_nr = i
    protoDf_list  = ExportMethods.append_shiftOccurence_toDf(shiftOccurence, protoDf_list, block_nr)

ExportMethods.generate_dfShiftOccurence(protoDf_list, participant_nr)

"""