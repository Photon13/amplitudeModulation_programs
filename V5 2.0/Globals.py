from typing import List



class Globals:

    POSITIONEN = ["left", "middle", "right"] #keep!

    LED_COORDINATES = [(0, -25), (0, 0), (0, 25)]
    SPEAKER_COORDINATES = [(-35, 0), (0, 0), (35, 0)]

    FAM_A : float = 33.0
    FAM_B : float = 43.0
    FAM_C : float = 53.0
    FAM_LIST : List[float] = [FAM_A, FAM_B, FAM_C]

    N_BLOCKS : int = 5*4 # je 1 min

    VOLUME = 0.18



    COLORBLUE   = '\33[34m'
    COLORGREEN = "\033[0;32m"
    COLORRED    = '\33[31m'
    COLORCYAN = '\033[36m'
    COLORPURPLE = '\033[35m'
    COLORYELLOW = '\033[33m'
    COLORFAT = '\033[1m'
    COLOREND = '\033[0m'


    


        