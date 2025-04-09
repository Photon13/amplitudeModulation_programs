import os
from pathlib import Path

class Globals():

    LED_COORDINATES = [(0, -25), (0, 0), (0, 25)]
    SPEAKER_COORDINATES = [(-35, 0), (0, 0), (35, 0)]

    FAM_A_BASE = 7
    FAM_B_BASE = 9
    FAM_C_BASE = 11
    SHIFT = 6

    FAM_A_SHIFTED = FAM_A_BASE + SHIFT
    FAM_B_SHIFTED = FAM_B_BASE + SHIFT
    FAM_C_SHIFTED = FAM_C_BASE + SHIFT
    

    FAM_ABC_BASE_LIST = [FAM_A_BASE, FAM_B_BASE, FAM_C_BASE]
    FAM_ABC_SHIFTED_LIST = [FAM_A_SHIFTED, FAM_B_SHIFTED, FAM_C_SHIFTED]
     
    N_SUBBLOCKS = (1+15)    # (4*16 seconds = 64 seconds; 0.subblock: no shift) 
    N_BLOCKS = (2+16)        # (2 test blocks + (4 blocks per condition) | 4 conditions (i.e. target types))


    path_cwd = Path(os.getcwd())
    # folder .../amplitudeModulation_programs/pre-final-summarised-edition has to be opened !
    path_rcx = path_cwd / "pre_final"/"src"/"amp_mod_package_mxxk"/"data"/"rcx"/"standard_setup_long_pre_final.rcx"
    path_participantInfo = path_cwd / "participant information"
    def get_path_json1(participant_nr):
        path_json1 = Globals.path_participantInfo / f"participant_{participant_nr}_info_1.json"
        return path_json1