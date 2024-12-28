from datetime import *
import json
from pathlib import Path
import os
import re
import sys
import random
from typing import List

from Globals import Globals

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
    blockDict : dict # <block_name> : <shift position list>
    
    
    
    
    def __init__( self, participantNr : str ):

        self.nr = participantNr
        self.name = f"participant-{participantNr}"

        self.date = self.set_date() 
            # works, old date kept after reinitialisation

        self.n_blocks = Globals.N_BLOCKS
        self.n_subblocks = Globals.N_SUBBLOCKS

        self.targetList = self.generate_targetList()
        self.famDict = self.generate_famDict()
        self.blockDict = self.generate_blockDict()
        
   
   

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
    
    
    

    def generate_blockDict(self) -> dict:
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
    



    def export_participantInstance_toJson( self ) -> None:
        """ Writes attributes + values for single participant to Json txt file """

        savePath : Path = Globals.PATH_JSON_FOLDER / f"{self.name}.txt"
        #print(jsonData)
        with open( savePath, "w") as file:
            json.dump( self.__dict__, file, indent=4) 




    def check_if_Json_exists(participantNr : int) -> bool:
        """  Checks if Json with the given participant number exists
                returns True if exists
                returns False if does not exist   """

        savePath : Path = Globals.PATH_JSON_FOLDER / f"participant-{participantNr}.txt"

        if savePath.exists() == True:
            print(COLORRED + "Json already exists! Json will be used to read attributes." + COLOREND)
            return True
        else: 
            print(COLORGREEN + "Creating new participant ..." + COLOREND)
            return False

  


    @staticmethod
    def read_participantInformation_fromJson(participantNr : int) -> dict:
        """ Help method for init_participants_fromJson() """

        participantName : str = f"participant-{participantNr}"
        loadPath : Path = Globals.PATH_JSON_FOLDER / f"{participantName}.txt" 

        with open(loadPath, "r") as file:
            data = json.load(file) # type data = dict
        return data
    



    @staticmethod
    def init_singleParticipant_fromJson(participantNr : int) -> object:

        loadpath = Globals.PATH_JSON_FOLDER / "participant-{participantNr}.txt"
        data = Participant.read_participantInformation_fromJson( participantNr)
        participant = Participant(participantNr)
        participant.__dict__ = data
        print(COLORGREEN + "Participant successfully reinitiated. " + COLOREND + "(Message from init_singleParticipant_fromJson(participantNr : int))")
        return participant




    @staticmethod
    def init_participants_fromJson() -> dict:
        """ Function for reinitiation of participants for data analysis.
            Participants are stored in a dictionary as participantMap["participant-{participantNr}"]"""
        
        dirList : List[str] = os.listdir(Globals.PATH_JSON_FOLDER)
        fileList : List[str] = []

        for entry in dirList:
            if os.path.isfile(Globals.PATH_JSON_FOLDER / entry) == True:
                fileList.append(entry)
        print(  COLORBLUE + "List of Json files: " + COLOREND 
                + f"\n{fileList}" )
        print( COLORBLUE + "Number of Json files: " + COLOREND
               + f"\n{len(fileList)}" )

        participantMap : dict = {}

        for fileName in fileList:
            participantNr = re.search(r"\d+", fileName).group()
                # re.search(<pattern>, <str>") finds first occurence of pattern in String 
                # r"\d+" matches an int with any number of digits
                # group() converts match obj into str
            data = Participant.read_participantInformation_fromJson( participantNr)
            participantMap[f"participant-{participantNr}"] = Participant(participantNr)
            participantMap[f"participant-{participantNr}"].__dict__ = data
            
            #print(f"Entry participant map [nr]: \n{participantMap[f"participant-{participantNr}"]}\n")
        
        #print(COLORBLUE + "Participant Map:" + COLOREND)
        #for key in participantMap:
        #    print(f"{key} : {participantMap[key]}")
        return participantMap
    
 
  

    """
    @staticmethod
    def generate_famDict() -> dict:
        # Randomly assigns famA, famB, famC to famLeft, famMiddle, famRight
        #    and puts latter ones and shift into dict 
        intList : list[int]= [0, 1, 2]
        intList = random.sample(intList, k = 3)

        famDict : dict = {}
        famDict["famLeft_base"] = Globals.FAM_ABC_BASE_LIST[   intList[0] ]
        famDict["famMiddle_base"] = Globals.FAM_ABC_BASE_LIST[ intList[1] ]
        famDict["famRight_base"] = Globals.FAM_ABC_BASE_LIST[  intList[2] ]

        famDict["shiftA"] = Globals.SHIFT_A
        famDict["shiftB"] = Globals.SHIFT_B
        famDict["shiftC"] = Globals.SHIFT_C

        famDict["famLeft_shifted"] = Globals.FAM_ABC_SHIFTED_LIST[   intList[0] ]
        famDict["famMiddle_shifted"] = Globals.FAM_ABC_SHIFTED_LIST[ intList[1] ]
        famDict["famRight_shifted"] = Globals.FAM_ABC_SHIFTED_LIST[  intList[2] ]

        return famDict
    """     

    
       
        