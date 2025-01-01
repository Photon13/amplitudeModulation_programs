from datetime import *
import json
from pathlib import Path
import os
import re
import sys
import random
from typing import List

from Globals import Globals
from Dateien import Dateien

COLORBLUE = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED = '\33[31m'
COLOREND = '\033[0m'




class Participant:
    
    nr: str
    name : str

    date: str

    n_blocks: int
    n_subblocks: int

    targetList : List[str]
    famDict : dict
    blockShiftDict : dict # <block_name> : <shift position list>

    blocksWithConditionDict : dict
    
    
    
    
    def __init__( self, participantNr : str ):

        self.nr = participantNr
        self.name = f"participant-{participantNr}"

        self.date = self.set_date() 
            # works, old date kept after reinitialisation

        self.n_blocks = Globals.N_BLOCKS
        self.n_subblocks = Globals.N_SUBBLOCKS

        self.targetList = self.generate_targetList()
        self.famDict = self.generate_famDict()
        self.blockShiftDict = self.generate_blockShiftDict()

        self.blocksWithConditionDict = self.findAllBlocks_withSpecificCondition()
        
   
   

    def set_date( self ) -> str:
        """ Sets self.date to today's date """

        currentDate : date = date.today()
            # datetime.date.today()
        currentDate : str = currentDate.strftime( '%Y-%m-%d')
        return currentDate




    def set_date_manually( self, dateString: str ) -> None: 
        """ If participant's session is on > 1 days 
            or the computers date is wrong 
            the date can be set manually
        
            single date format: YYYY-mm-dd
            multiple dates format: YYYY-mm-dd-YYYY-mm-dd """

        self.date = dateString

    
    
    
    def generate_targetList(self) -> List[str]: 

        targetList : list[str] = []
        targetList.append(random.choice(["left", "middle", "right"])) 
            # 0.block: target is single speaker 
                # test block
        targetList.append("both") 
            # 1.block: target is both (left + right speaker)
                # test block
        
        k = ((self.n_blocks)-2) * (1.0/4.0)
        k = int (k)

        while True:
            if (k/4 != 1) or (k/4 != 2) or (k/4 != 3) or (k/4 != 4) or (k/4 != 5):
                break
            else:
                print(  COLORRED + "Problem occured in generate_targetList(): " 
                        + "Number of blocks probably not multiple of 4"
                        +" ... Check value in Globals" + COLOREND)
                sys.exit()

        targetsNormalBlocksUnshuffled = []
        targetsNormalBlocksUnshuffled.extend( k*["left"]   ) 
        targetsNormalBlocksUnshuffled.extend( k*["middle"] )
        targetsNormalBlocksUnshuffled.extend( k*["right"]  )
        targetsNormalBlocksUnshuffled.extend( k*["both"]   )
            # non-test blocks
        
        targetsNormalBlocksShuffled = random.sample(
            targetsNormalBlocksUnshuffled, 
            k = self.n_subblocks
        )       # randomise order of entries

        targetList = targetList + targetsNormalBlocksShuffled
        return targetList
    
    
    

    def generate_blockShiftDict(self) -> dict:
        """ Creates a dict with <block name> : <list shift position> """
        blockDict : dict = {}

        for i in range(self.n_blocks):
            blockDict[f"block_{i}"] = Participant.generate_randomShiftOccurenceList()

                # blockDict[f"block_{i}"] = shift position
        return blockDict
    


    
    @staticmethod
    def generate_randomShiftOccurenceList() -> List[str]:
        """ Help method for generate_blockDict() """
        randomShiftOccurenceList = random.choices(["l", "m", "r"], k = (Globals.N_SUBBLOCKS -1)) # excl. 0.subblock
        randomShiftOccurenceList = ["n"]+ randomShiftOccurenceList # 0. subblock no shift

        return randomShiftOccurenceList
    
    
    
   
    def assignFams_helpMethod(self, listFromGlobals : List[int] ) -> List[int]:
        """ Help method for Participant.generate_famDict() 
                Position of frequency is pseudo-randomised    """

        pseudoRandomisedFamList : List[int] 
        a : int = listFromGlobals[0]
        b : int = listFromGlobals[1]
        c : int = listFromGlobals[2]

        # participant.nr ==   (x*6) + z   =>   nr/6 == x + z/6   =>   nr%6 == z
        # (x*6) is a multiple of 6   ;   here z is the remainder of the division 
        # x == {0, 1, 2, ..., u}   ;   z == {0, 1, 2, 3, 4, 5}

        if( self.nr % 6 == 1):  # True for .nr == 1 || 7 || 13 || ...
            pseudoRandomisedFamList = [b, a, c] # famMiddle == famA

        elif( self.nr % 6 == 2): # True for .nr == 2 || 8 || 14 || ...
            pseudoRandomisedFamList = [c, a, b]  # famMiddle == famA
        
        elif( self.nr % 6 == 3): # True for .nr == 3 || 9 || 15 || ...
            pseudoRandomisedFamList = [a, b, c]  # famMiddle == famB

        elif( self.nr % 6 == 4): # True for .nr == 4 || 10 || 16 || ...
            pseudoRandomisedFamList = [c, b, a]  # famMiddle == famB

        elif( self.nr % 6 == 5): # True for .nr == 5 || 11 || 17 || ...
            pseudoRandomisedFamList = [a, c, b]  # famMiddle == famC

        elif( self.nr % 6 == 0): # True for .nr == 6 || 12 || 16 || ...
            pseudoRandomisedFamList = [b, c, a]  # famMiddle == famC

        else :
            print( COLORRED + ".famList could not be generated! " + COLOREND + "(Message from assignFams_helpMethod(self, listFromGlobals))")
            sys.exit()

        return pseudoRandomisedFamList




    def generate_famDict(self) -> dict:

        famDict : dict = {}

        pseudoRandomised_baseFamList : List[int] = self.assignFams_helpMethod( Globals.FAM_ABC_BASE_LIST )

        famDict["famLeft_base"] = pseudoRandomised_baseFamList[0] 
        famDict["famMiddle_base"] = pseudoRandomised_baseFamList[1] 
        famDict["famRight_base"] = pseudoRandomised_baseFamList[2] 

        pseudoRandomised_shiftedFamList : List[int] = self.assignFams_helpMethod( Globals.FAM_ABC_SHIFTED_LIST )

        famDict["famLeft_shifted"] = pseudoRandomised_shiftedFamList[0]
        famDict["famMiddle_shifted"] = pseudoRandomised_shiftedFamList[1]
        famDict["famRight_shifted"] = pseudoRandomised_shiftedFamList[2] 

        pseudoRandomised_shiftList : List[int] = self.assignFams_helpMethod( Globals.SHIFT_ABC_LIST )

        famDict["shiftLeft"] = pseudoRandomised_shiftList[0]
        famDict["shiftMiddle"] = pseudoRandomised_shiftList[1]
        famDict["shiftRight"] = pseudoRandomised_shiftList[2]

        return famDict
    



    def findAllBlocks_withSpecificCondition(self) -> None:

        blocksWithConditionDict : dict = {}

        blockNrsLeft : list[int] = [index for index, entry in enumerate(self.targetList) if entry == "left"] # does (i, x) work?
        blockNrsMiddle : list[int] = [index for index, entry in enumerate(self.targetList) if entry == "middle"]
        blockNrsRight : list[int] = [index for index, entry in enumerate(self.targetList) if entry == "right"]
        blockNrsBoth : list[int] = [index for index, entry in enumerate(self.targetList) if entry == "both"]
            # ´enumerate(<list>)´ returns iterable containing (<index>, <entry>) for each item in list
            # ´index for (index, entry) in <iterable> if entry == <"irgendwas">´ picks all indices for whose the entry is "irgendwas"

        blocksWithConditionDict["single_leftTarget"] = blockNrsLeft
        blocksWithConditionDict["single_middleTarget"] = blockNrsMiddle
        blocksWithConditionDict["single_rightTarget"] = blockNrsRight
        blocksWithConditionDict["bothTarget"] = blockNrsBoth

        return blocksWithConditionDict 



    #-------JSON-------#


    @staticmethod
    def check_if_Json_exists(participantNr : int, globals : object) -> bool:
        """  Checks if Json with the given participant number exists
                returns True if exists
                returns False if does not exist   """

        savePath : Path = globals.get_pathJsonFolder() / f"participant-{participantNr}.txt"

        if savePath.exists() == True:
            print(COLORRED + "Json already exists! Json will be used to read attributes." + COLOREND)
            return True
        else: 
            print(COLORGREEN + "Creating new participant ..." + COLOREND)
            return False

  

    @staticmethod
    def export_participantInstance_toJson( participant : object, globals : object ) -> None:
        """ Writes attributes + values for single participant to Json txt file """

        savePath : Path = globals.get_pathJsonFolder() / f"{participant.name}.txt"
        
        with open( savePath, "w") as file:
            json.dump( participant.__dict__, file, indent=4)




    @staticmethod
    def read_participantInformation_fromJson(globals : object, fileNameJson : str) -> dict:
        """ Help method for init_participants_fromJson() """

        loadPath : Path = globals.get_pathJsonFolder() / fileNameJson

        with open(loadPath, "r") as file:
            jsonData = json.load(file) # type data = dict
        return jsonData
    



    @staticmethod
    def init_singleParticipant_fromJson(participantNr : int, globals : object) -> object:

        jsonData = Participant.read_participantInformation_fromJson( globals, f"participant-{participantNr}.txt" )
        participant = Participant(participantNr)
        participant.__dict__ = jsonData

        print(COLORGREEN + "Participant successfully reinitiated. " + COLOREND + "Message from  Dateien.init_singleParticipant_fromJson()")
        return participant  

    
       
        