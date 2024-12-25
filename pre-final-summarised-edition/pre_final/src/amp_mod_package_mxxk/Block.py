import random
import numpy as np
from typing import List

from Globals import Globals
from Participant import Participant

class Block(Participant):

    name: str
    target: str
    ShiftOccurence: List[str]
    
    #nrSeqLeft: List[] ; later int[]
    #nrSeqMiddle: List[] ; later int[]
    #nrSeqRight: List[] ; later int[]
    #_______________________________________________________________________

    # called via Participant.set_blockDict()
    def __init__(self, blockName):
        self.name = blockName
        self.target = "not_set" # target is assigned in Participant class

        self.shiftOccurence = []
        
        self.nrSeqLeft = []
        self.nrSeqMiddle = []
        self.nrSeqRight = []
    #_______________________________________________________________________    

    def set_shiftOccurence(self): # works as desired
        shiftOccurence = random.choices(["left", "middle", "right"], k = (Globals.N_SUBBLOCKS -1)) # excl. 0.subblock
        self.shiftOccurence = ["no"]+ shiftOccurence # 0. subblock no shift

    def get_shiftOccurence(self):
        return self.shiftOccurence
    #_______________________________________________________________________
    
    def set_nrSeqs(self):
        """     left no shift:   1  ;  left shift:   2
                middle no shift: 3  ;  middle shift: 4
                right no shift:  5  ;  right shift:  6      """
        
        # 0. subblock (no shift at all):
        nrSeqLeft = [1,1,1,1]
        nrSeqMiddle = [3,3,3,3]
        nrSeqRight = [5,5,5,5]

        # other subblocks:
        for index in range( 1, len(self.shiftOccurence) ): # 0. entry skipped

            if( self.shiftOccurence[index] == "left" ):
                nrSeqLeft = nrSeqLeft + [2,2,2,2] # shift
                nrSeqMiddle = nrSeqMiddle + [3,3,3,3] # no shift
                nrSeqRight = nrSeqRight + [5,5,5,5] # no shift

            elif( self.shiftOccurence[index] == "middle" ):
                nrSeqLeft = nrSeqLeft + [1,1,1,1] # no shift
                nrSeqMiddle = nrSeqMiddle + [4,4,4,4] # shift
                nrSeqRight = nrSeqRight + [5,5,5,5] # no shift

            elif( self.shiftOccurence[index] == "right" ):
                nrSeqLeft = nrSeqLeft + [1,1,1,1] # no shift
                nrSeqMiddle = nrSeqMiddle + [3,3,3,3] # no shift
                nrSeqRight = nrSeqRight + [6,6,6,6] # shift

            else: 
                print("\nCAVE: nrSeq couldn't be generated.")

        self.nrSeqLeft = np.array(nrSeqLeft).astype('int32') # nrSeqLeft = np.append(0, nrSeqLeft) #?
        self.nrSeqMiddle = np.array(nrSeqMiddle).astype('int32')  # nrSeqMiddle = np.append(0, nrSeqMiddle) #?
        self.nrSeqRight = np.array(nrSeqRight).astype('int32') # nrSeqRight = np.append(0, nrSeqRight) #?
        
    def get_nrSeqs(self):
        #print(participant.blockDict[f"block_{i}"].nrSeqLeft)
        #print(participant.blockDict[f"block_{i}"].nrSeqMiddle)
        #print(participant.blockDict[f"block_{i}"].nrSeqRight)
        return self.nrSeqLeft, self.nrSeqMiddle, self.nrSeqRight 
    #_______________________________________________________________________


        

