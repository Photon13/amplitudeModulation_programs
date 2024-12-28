import random
import numpy as np
from typing import List
from pathlib import Path

from Globals import Globals

COLORBLUE = '\33[34m'
COLORRED = '\33[31m'
COLOREND = '\033[0m'

class Auswertung:

    def calculate_power(blockNr : int):
        # calculate time/eeg samples for the respective block
        return power
        

    def calulate_powerForAllBlocks(participant : object, eegPath : Path, blocksWithConditionDict : dict) -> dict:
        # find proper EEG snippets
        famLeft : int = participant.famDict["famLeft"]
        famMiddle : int = participant.famDict["famMiddle"]
        famRight : int = participant.famDict["famRight"]
    

        powerDict : dict = {}

        meanP_single_leftTarget : float = 0.0
        for blockNr in blocksWithConditionDict["single_leftTarget"]:
            power = calculate_power(blockNr, eegPath)
            meanP_single_leftTarget = meanP_single_leftTarget + power

        """ SAME FOR THE OTHER CONDITIONS:
        powerDict["meanP_single_middleTarget"] =
        powerDict["meanP_single_rightTarget"] =
        powerDict["meanP_bothTarget"] =
        """

        return powerDict
    

    
    #def berechne_Power(participant : object) -> dict:



    def findAllBlocks_withSpecificCondition(participant : object) -> dict:

        blocksWithConditionDict : dict = {}

        blockNrsLeft : list[int] = [index for index, entry in enumerate(participant.targetList) if entry == "left"] # does (i, x) work?
        blockNrsMiddle : list[int] = [index for index, entry in enumerate(participant.targetList) if entry == "middle"]
        blockNrsRight : list[int] = [index for index, entry in enumerate(participant.targetList) if entry == "right"]
        blockNrsBoth : list[int] = [index for index, entry in enumerate(participant.targetList) if entry == "both"]
            # ´enumerate(<list>)´ returns iterable containing (<index>, <entry>) for each item in list
            # ´index for (index, entry) in <iterable> if entry == <"irgendwas">´ picks all indices for whose the entry is "irgendwas"

        blocksWithConditionDict["single_leftTarget"] = blockNrsLeft
        blocksWithConditionDict["single_middleTarget"] = blockNrsMiddle
        blocksWithConditionDict["single_rightTarget"] = blockNrsRight
        blocksWithConditionDict["bothTarget"] = blockNrsBoth

        return blocksWithConditionDict
    
    #def
    #    frequency : int = #
    #    dataPath : Path = #
    #    get_Power(dataPath, condition, frequency)
