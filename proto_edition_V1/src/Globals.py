import os
from pathlib import Path




class Globals():
    """ Contains global variables/ constants for proto_edition_V1 """

    # Coordinates for freefield
    LED_COORDINATES = [(0, -25), (0, 0), (0, 25)]
    SPEAKER_COORDINATES = [(-35, 0), (0, 0), (35, 0)]
    
    #horizontalSpeakerCoordinatesList : List(str) = [
    #    (-52.5, 0), (-35.5, 0), (-17.5, 0), 
    #    (0, 0), 
    #    (17.5), (35.5, 0), (52.5, 0)
    #]

    # Frequencies of amplitude modulation
    FAM_A_BASE = 3
    FAM_B_BASE = 7
    FAM_C_BASE = 13

    # Δfrequency // shift is added to base fam
    SHIFT_A = 4
    SHIFT_B = 4
    SHIFT_C = 4


    FAM_A_SHIFTED = FAM_A_BASE + SHIFT_A
    FAM_B_SHIFTED = FAM_B_BASE + SHIFT_B
    FAM_C_SHIFTED = FAM_C_BASE + SHIFT_C
    
    FAM_ABC_BASE_LIST = [FAM_A_BASE, FAM_B_BASE, FAM_C_BASE]
    FAM_ABC_SHIFTED_LIST = [FAM_A_SHIFTED, FAM_B_SHIFTED, FAM_C_SHIFTED]
    SHIFT_ABC_LIST = [SHIFT_A, SHIFT_B, SHIFT_C]
    



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
