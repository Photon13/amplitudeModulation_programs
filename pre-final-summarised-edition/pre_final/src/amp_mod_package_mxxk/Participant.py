import random
from typing import List

from Globals import Globals
from Block import Block

class Participant:

    """ Attributes """
    name: str
    fam_LMR_base_list: List[int]
    fam_LMR_shifted_list: List[int]
    blockDict: dict[str, object]
    # attributes of block belonging to the participant can be called via:
    # <instance participant>.blockDict["<block name>"].<attribute of block>
    # e.g. participant77.blockDict["block_0"].target returns target of block 0 of participant77

    """ Constructor """
    def __init__(self, participantNr):
        self.name = f"participant{participantNr}"
        self.fam_LMR_base_list = []
        self.fam_LMR_shifted_list = []
        self.blockDict = {}
        

    """ Method to randomise speakers 
        assigns frequencies to left, middle and right speaker
        for all base (unshifted) and shifted sound frequencies """
    def set_randomisedSpeakerFrequencies(self):
        self.fam_LMR_base_list = random.sample(Globals.FAM_ABC_BASE_LIST, k=3)

        self.fam_LMR_shifted_list = ( [ (self.fam_LMR_base_list[0] + Globals.SHIFT),
                                        (self.fam_LMR_base_list[1] + Globals.SHIFT),
                                        (self.fam_LMR_base_list[2] + Globals.SHIFT) ]
        )
    
    def get_speakerFrequencies_LMR(self):
        print( "\n(base,shifted):" )
        print( f"A:({self.fam_LMR_base_list[0]}, {self.fam_LMR_shifted_list[0]})" )
        print( f"B:({self.fam_LMR_base_list[1]}, {self.fam_LMR_shifted_list[1]})" )
        print( f"C:({self.fam_LMR_base_list[2]}, {self.fam_LMR_shifted_list[2]})" )
        return self.fam_LMR_base_list, self.fam_LMR_shifted_list 


    def set_blockDict(self):
        blockList = []
        for i in range (Globals.N_BLOCKS):
            blockList = blockList + [f"block_{i}"] #blockList.append(f"block_{i}")
    
        # dictionary[String, Block]
        # dictionary[key, value]
        # e.g. blockDict = {"block_0", <instance of block_0>}
        self.blockDict = {x: Block(blockName = x) for x in blockList} 
    
    def get_blockDict(self):
        return self.blockDict
    

    def set_targetList(self): # works as desired
        # 0.subblock: no target:
        targetList = []
        targetList.append(random.choice(["left", "middle", "right"]))
        targetList.append("both")

        k=4
        targetsNormalBlocksUnshuffled = []
        targetsNormalBlocksUnshuffled.extend( 4*["left"] ) 
        targetsNormalBlocksUnshuffled.extend( 4*["middle"] )
        targetsNormalBlocksUnshuffled.extend( 4*["right"] )
        targetsNormalBlocksUnshuffled.extend( 4*["both"] )

        # randomise order of entries:
        targetsNormalBlocksShuffled = random.sample(targetsNormalBlocksUnshuffled, k=Globals.N_SUBBLOCKS)

        self.targetList = targetList + targetsNormalBlocksShuffled
    
    def get_targetList(self):
        print(self.targetList)
        return self.targetList
    

    def set_targetsToAllBlocks(self): # seems to work
        for i in range(Globals.N_BLOCKS):
            self.blockDict[f"block_{i}"].target = self.targetList[i]

    def get_targetOfBlockXY(self, block_nr):
        print(self.blockDict[f"block_{block_nr}"].target)
        return self.blockDict[f"block_{block_nr}"].target

"""
METHOD SUMMARY:

participant_nr = 66
participant = Participant(participant_nr)
participant.set_randomisedSpeakerFrequencies()
#participant.get_speakerFrequencies_ABC()

participant.set_blockDict()
#participant.get_blockDict()

participant.set_targetList()
#participant.get_targetList()

participant.set_targetsToAllBlocks()

# block_nr = 0
# participant.get_targetOfBlockXY(block_nr)

"""





