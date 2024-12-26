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
    #______________________________________________________________________
    
    nr: str
    name : str

    date: str

    n_blocks: int
    n_subblocks: int

    targetList : List[str]
    famDict : dict
    blockDict : dict # <block_name> : <shift position list>
    

    #______________________________________________________________________
    
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
        
    #______________________________________________________________________

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


    #______________________________________________________________________
    
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
    #______________________________________________________________________
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
    #______________________________________________________________________
    
    @staticmethod
    def generate_famDict() -> dict:
        """ Randomly assigns famA, famB, famC to famLeft, famMiddle, famRight
            and puts latter ones and shift into dict """
        intList : list[int]= [0, 1, 2]
        intList = random.sample(intList, k = 3)

        famDict : dict = {}
        famDict["famLeft"] = Globals.FAM_ABC_BASE_LIST[intList[0]]
        famDict["famMiddle"] = Globals.FAM_ABC_BASE_LIST[intList[1]]
        famDict["famRight"] = Globals.FAM_ABC_BASE_LIST[intList[2]]
        famDict["shift"] = Globals.SHIFT

        return famDict
    #______________________________________________________________________

    def export_participantInstance_toJson( self ) -> None:
        """ Writes attributes + values for single participant to Json txt file """

        self.check_if_Json_exists()
        savePath : Path = Globals.PATH_JSON_FOLDER / f"{self.name}.txt"
        #print(jsonData)
        with open( savePath, "w") as file:
            json.dump( self.__dict__, file, indent=4) 

    def check_if_Json_exists(self) -> None:
        """ Help method for export_participantInformation_toJson: 
                Checks if Json with the set participant number exists
                aborts program if Json exists """

        savePath : Path = Globals.PATH_JSON_FOLDER / f"{self.name}.txt"
        if savePath.exists() == True:
            print(COLORRED + "Json already exists! Please change participant number and restart." + COLOREND)
            sys.exit()
    #______________________________________________________________________

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
    
    #______________________________________________________________________        
        