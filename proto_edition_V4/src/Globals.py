from typing import List

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'




class Globals:

    POSITIONEN = ["left", "middle", "right"] #keep!

    LED_COORDINATES = [(0, -25), (0, 0), (0, 25)]
    SPEAKER_COORDINATES = [(-35, 0), (0, 0), (35, 0)]

    FAM_A_BASE : float = 33.0
    FAM_B_BASE : float = 43.0
    FAM_C_BASE : float = 53.0

    FAM_LIST : List[float] = [FAM_A_BASE, FAM_B_BASE, FAM_C_BASE]

    F_NOTCH : float = 50.0
    F_MIN_BANDPASS : float = 1.0
    F_MAX_BANDPASS : float = 100.0

    #____old____#
    #N_BLOCKS : int = (2 + 4*4) # 18
    #N_SUBBLOCKS : int = (1 + 20) # 21 subblocks * 4 sec = 84 sec
    # 18 blocks * 21 subblocks * 4 sec = 1512 sec = 25.2 min

    N_SUPERBLOCKS : int = 16   # total   # superblocks do NOT contain testblocks
    N_BLOCKS : int = 32        # total   # without testBlocks
    N_SUBBLOCKS : int = 10      # per block
    # 1 block = 10 subblocks * 4 sec = 40 sec
    # 1 superblock = 2 blocks = 80 sec
    # 16 superblocks = 32 blocks = 1280 sec = 21.33 min
    # + 40 sec test

    # per condition 8 blocks


    # 5,6,RX82,-35,37.5,,
    # 20,4,RX81,0,37.5,,
    # 23,1,RX81,0,0,16,RX81
    # 26,14,RX81,0,-37.5,,

    


        