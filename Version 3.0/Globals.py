import os
from pathlib import Path
from typing import List

class Globals:

    LED_COORDINATES     = [(0, -25), (0, 0), (0, 25)]
    SPEAKER_COORDINATES = [(-35, 0), (0, 0), (35, 0)]

    FAM_A : float = 35.9
    FAM_B : float = 39.7
    FAM_C : float = 43.2
    FAM_LIST : List[float] = [FAM_A, FAM_B, FAM_C]

    N_BLOCKS     : int = 72   #(3 trials * 6 freqCombs * 4 conditions)
    BLOCK_LENGTH : int = 30   #[sec] 

    VOLUME : float = 0.18

    # diff = 4.8, 4.4