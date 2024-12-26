import os
from pathlib import Path

class Globals():
    """ Contains global variables/ constants for proto_edition_V1 """

    # Coordinates for freefield
    LED_COORDINATES = [(0, -25), (0, 0), (0, 25)]
    SPEAKER_COORDINATES = [(-35, 0), (0, 0), (35, 0)]

    # Frequencies of amplitude modulation
    FAM_A_BASE = 3
    FAM_B_BASE = 7
    FAM_C_BASE = 13
    SHIFT = 4

    FAM_A_SHIFTED = FAM_A_BASE + SHIFT
    FAM_B_SHIFTED = FAM_B_BASE + SHIFT
    FAM_C_SHIFTED = FAM_C_BASE + SHIFT
    
    FAM_ABC_BASE_LIST = [FAM_A_BASE, FAM_B_BASE, FAM_C_BASE]
    FAM_ABC_SHIFTED_LIST = [FAM_A_SHIFTED, FAM_B_SHIFTED, FAM_C_SHIFTED]
    
    # Number of blocks and subblocks
    N_SUBBLOCKS = (1+15)   
        # 16 subblocks, 4 seconds resp.
        # 1st second: shifted sound; 2.-4. second: unshifted sound 
        # in sum: 1 block = 64 seconds (4 sec * 16)
        # CAVE: 0.subblock: always unshifted ! 
        #
    N_BLOCKS = (2+16)       
        # 2 test blocks + 16 normal blocks
        # 4 conditions (i.e. target types)), 4 blocks resp.

    # Paths
    PATH_CWD = Path(os.getcwd())
        # cwd must be: "...\\amplitudeModulation_programs\\proto_edition_V1"
    
    PATH_RCX_FILE = PATH_CWD /"data"/"rcx"/"standard_setup_long_pre_final.rcx"
        # path to rcx files
    
    PATH_JSON_FOLDER = PATH_CWD / "participant_json"
        # path to json files



    #def get_path_json1(participant_nr):
    #    path_json1 = Globals.path_participantInfo / f"participant_{participant_nr}_info_1.json"
    #    return path_json1