from typing import List

from Globals import Globals
from Experiment import Experiment





class test_amPinknoise:
    """ rechts #### -> aendern """

    #BASISFREQUENZEN:
    famLeft_basis : int = 7 # [Hz]                                              ####
    famMiddle_basis : int = 11 # [Hz]                                           ####
    famRight_basis : int = 13 # [Hz]                                            ####

    famLMR_basis : List[int] = [famLeft_basis, famMiddle_basis, famRight_basis]

    #GESHIFTETE FREQUENZEN:
    shift : int = 4 # [Hz]                                                      ####

    famLeft_shifted : int = famLeft_basis + shift # [Hz]
    famMiddle_shifted : int = famMiddle_basis + shift # [Hz]
    famRight_shifted : int = famRight_basis + shift # [Hz]

    famLMR_shift : List[int] = [famLeft_shifted, famMiddle_shifted, famRight_shifted] 



    #DAUER SHIFT:
    deltaT_shift : int = 1 # [sec] 

    #DAUER BASIS:
    deltaT_nonShift : int = 3 # [sec] 

    #DAUER SUBBLOCK:
    deltaT_subB : int = deltaT_shift + deltaT_nonShift # [sec] 


    #ANZAHL SUBBLOECKE:
    n_subB : int = (1+15)                                                       ####

    #DAUER SUBBLOCK:
    deltaT_subB : int = n_subB * deltaT_subB # [sec]






  