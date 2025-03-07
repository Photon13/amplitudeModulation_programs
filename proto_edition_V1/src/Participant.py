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

    
    
    
    def generate_targetList( self ) -> List[str]: 

        targetList : list[str] = []     
                                                
        targetList.append(random.choice(["left", "middle", "right"]))           # 0.block (test block): target is single speaker            
        targetList.append("both")                                               # 1.block (test block): target is both (left + right speaker)


        j : int = 4                                                             # nr of blocks per condition

        targetsNormalBlocksUnshuffled = []                                      # non-test blocks
        targetsNormalBlocksUnshuffled.extend( j*["left"]   ) 
        targetsNormalBlocksUnshuffled.extend( j*["middle"] )
        targetsNormalBlocksUnshuffled.extend( j*["right"]  )
        targetsNormalBlocksUnshuffled.extend( j*["both"]   )
            
        targetsNormalBlocksShuffled = random.sample( targetsNormalBlocksUnshuffled, k = 4*j)          # randomise order of entries

        targetList = targetList + targetsNormalBlocksShuffled                                                   # concatenate test and non-test targets

        return targetList
    
    
    

    def generate_blockShiftDict( self ) -> dict:
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
    
    
    

    def generate_famDict( self ) -> dict:
        famDict : dict = {}

        helpList : List[int] = [0,1,2]
        shuffledHelpList = random.sample(helpList, k=3)

        
        famDict["famLeft_base"] =   Globals.FAM_ABC_BASE_LIST[ shuffledHelpList[0] ]
        famDict["famMiddle_base"] = Globals.FAM_ABC_BASE_LIST[ shuffledHelpList[1] ] 
        famDict["famRight_base"] =  Globals.FAM_ABC_BASE_LIST[ shuffledHelpList[2] ] 

        famDict["shiftLeft"] =      Globals.SHIFT_ABC_LIST[ shuffledHelpList[0] ]
        famDict["shiftMiddle"] =    Globals.SHIFT_ABC_LIST[ shuffledHelpList[1] ]
        famDict["shiftRight"] =     Globals.SHIFT_ABC_LIST[ shuffledHelpList[2] ]

        famDict["famLeft_shifted"] =    famDict["famLeft_base"]     + famDict["shiftLeft"]
        famDict["famMiddle_shifted"] =  famDict["famMiddle_base"]   + famDict["shiftMiddle"]
        famDict["famRight_shifted"] =   famDict["famRight_base"]    + famDict["shiftRight"] 

        return famDict




    def findAllBlocks_withSpecificCondition( self ) -> None:

        blocksWithConditionDict : dict = {}

        blockNrsLeft : list[int] = [index for index, entry in enumerate(self.targetList) if entry == "left"] # does (i, x) work?
        blockNrsMiddle : list[int] = [index for index, entry in enumerate(self.targetList) if entry == "middle"]
        blockNrsRight : list[int] = [index for index, entry in enumerate(self.targetList) if entry == "right"]
        blockNrsBoth : list[int] = [index for index, entry in enumerate(self.targetList) if entry == "both"]
            # enumerate(<list>) 
            #   returns iterable containing (<index>, <entry>) for each item in list
            # index for (index, entry) in <iterable> if entry == <"irgendwas">
            #   picks all indices for whose the entry is "irgendwas"

        blocksWithConditionDict["single_leftTarget"] = blockNrsLeft
        blocksWithConditionDict["single_middleTarget"] = blockNrsMiddle
        blocksWithConditionDict["single_rightTarget"] = blockNrsRight
        blocksWithConditionDict["bothTarget"] = blockNrsBoth

        return blocksWithConditionDict 



    #-------JSON-------#


    @staticmethod
    def check_if_Json_exists( participantNr : int, globals : object ) -> bool:
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
    def read_participantInformation_fromJson( globals : object, fileNameJson : str ) -> dict:
        """ Help method for init_participants_fromJson() """

        loadPath : Path = globals.get_pathJsonFolder() / fileNameJson

        with open(loadPath, "r") as file:
            jsonData = json.load(file) # type data = dict
        return jsonData
    



    @staticmethod
    def init_singleParticipant_fromJson( participantNr : int, globals : object ) -> object:

        jsonData = Participant.read_participantInformation_fromJson( globals, f"participant-{participantNr}.txt" )
        participant = Participant(participantNr)
        participant.__dict__ = jsonData

        print(COLORGREEN + "Participant successfully reinitiated. " + COLOREND + "Message from  Dateien.init_singleParticipant_fromJson()")
        return participant  
    

    
       
        