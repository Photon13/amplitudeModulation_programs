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

    LED_COORDINATES = [(0, -25), (0, 0), (0, 25)]
    SPEAKER_COORDINATES = [(-35, 0), (0, 0), (35, 0)]

    FAM_A_BASE : float = 35.3
    FAM_B_BASE : float = 40.0
    FAM_C_BASE : float = 44.7

    FAM_LIST : List[float] = [FAM_A_BASE, FAM_B_BASE, FAM_C_BASE]

    F_NOTCH : float = 50.0
    F_MIN_BANDPASS : float = 1.0
    F_MAX_BANDPASS : float = 100.0

    N_BLOCKS : int = (2 + 4*4) # 18
    N_SUBBLOCKS : int = (1 + 20) # 21 subblocks * 4 sec = 84 sec
    # 18 blocks * 21 subblocks * 4 sec = 1512 sec = 25.2 min



        