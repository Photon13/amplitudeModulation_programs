import random
from typing import List
import json
from datetime import datetime

from Globals import Globals
from Block import Block

class ParticipantHelpMethods:
    
    """ P0. Constructor """
    def __init__(self, participantNr):
        self.name = f"participant_{participantNr}"
        self.date = datetime.today().strftime('%Y%m%d')

        self.fam_LMR_base_list = []
        self.fam_LMR_shifted_list = []
        self.blockDict = {}
        
        # Block constructor called via Participant.set_blockDict()
    #______________________________________________________________________________________________________________________________________________________________

    """ P1. Assign speaker identity to Participant instance:    
                Method to randomise speakers: 
                    assigns frequencies to left, middle and right speaker
                    for all base (unshifted) and shifted sound frequencies  """
    def set_speakerFrequencies_LMR(self):
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
    #______________________________________________________________________________________________________________________________________________________________
    
    """ B0. Initiating of Block instances 
            # Participant instance aggregates Block instances
            -> Block instances are auto-generated and thus must be called via dictionary:

                dictionary[key, value] (key = block name as str; value = instance of Block)
                    e.g.    blockDict = {   "block_0", <instance of block_0>, 
                                            "block_1", <instance of block_1>
                                                ...                              } """
    def set_blockDict(self):
        blockList = []
        for i in range (Globals.N_BLOCKS):
            blockList = blockList + [f"block_{i}"] #blockList.append(f"block_{i}")
        self.blockDict = {x: Block(blockName = x) for x in blockList} 
    
    def get_blockDict(self):
        return self.blockDict
    #______________________________________________________________________________________________________________________________________________________________
    
    """ B1. Assign target for each Block instance """
    def set_targetList(self): # works as desired
        targetList = []
        targetList.append(random.choice(["left", "middle", "right"])) # 0.block: test block: target is single speaker 
        targetList.append("both") # 1.block: test block: target is both (left + right speaker)

        # non-test blocks:
        k = ((Globals.N_BLOCKS)-2) * (1.0/4.0)
        k = int (k)
        targetsNormalBlocksUnshuffled = []
        targetsNormalBlocksUnshuffled.extend( 4*["left"]   ) 
        targetsNormalBlocksUnshuffled.extend( 4*["middle"] )
        targetsNormalBlocksUnshuffled.extend( 4*["right"]  )
        targetsNormalBlocksUnshuffled.extend( 4*["both"]   )

        # randomise order of entries:
        targetsNormalBlocksShuffled = random.sample(targetsNormalBlocksUnshuffled, k=Globals.N_SUBBLOCKS)

        self.targetList = targetList + targetsNormalBlocksShuffled
    
    def get_targetList(self):
        print(self.targetList)
        return self.targetList
    #______________________________________________________________________________________________________________________________________________________________
    """ B2. Assign target to each Block instance: """
    def set_targetsToAllBlocks(self): # seems to work
        for i in range(Globals.N_BLOCKS):
            self.blockDict[f"block_{i}"].target = self.targetList[i]

    def get_targetOfBlockXY(self, block_nr):
        print(self.blockDict[f"block_{block_nr}"].target)
        return self.blockDict[f"block_{block_nr}"].target
    #______________________________________________________________________________________________________________________________________________________________
    """ Z. wrapper for P0, P1, B0, B1, B2 : """
    def precreate_participant(participant_nr): # works as desired
        participant = ParticipantHelpMethods(participant_nr)
        participant.set_speakerFrequencies_LMR()
        participant.set_blockDict()
        participant.set_targetList()
        participant.set_targetsToAllBlocks()
        return participant
    #______________________________________________________________________________________________________________________________________________________________
    
    """ J. Export the Participant instance (incl. Block instances) to Json file """
    @staticmethod
    def export_participantInstance_asJson(participant, participant_nr):
        dict = { ".name" : participant.name ,
                 ".fam_LMR_base_list" : participant.fam_LMR_base_list , 
                 ".fam_LMR_shifted_list" : participant.fam_LMR_shifted_list ,
                 ".N_BLOCKS" : Globals.N_BLOCKS ,
                 ".N_SUBBLOCKS" : Globals.N_SUBBLOCKS   
        }

        for i in range(Globals.N_BLOCKS):
            dict[f".block_{i}.target"] = f"{participant.blockDict[f"block_{i}"].target}"
            dict[f".block_{i}.shiftOccurence"] = f"{participant.blockDict[f"block_{i}"].shiftOccurence}"
            dict[f".block_{i}.nrSeqLeft"] = f"{participant.blockDict[f"block_{i}"].nrSeqLeft}"
            dict[f".block_{i}.nrSeqMiddle"] = f"{participant.blockDict[f"block_{i}"].nrSeqMiddle}"
            dict[f".block_{i}.nrSeqRight"] = f"{participant.blockDict[f"block_{i}"].nrSeqRight}"
        
        print("{")
        for key, value in dict.items():
            print(f"{key} : {value}")
        print("}")

        save_path = Globals.get_path_json1(participant_nr)
        with open(save_path, 'w') as file:
            json.dump(dict, file, indent=4, separators=(",", ":"))
        print("\n    Json saved.")
#______________________________________________________________________________________________________________________________________________________________