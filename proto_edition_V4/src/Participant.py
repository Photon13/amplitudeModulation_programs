from Globals import Globals
from Sequences import Sequences

from typing import List


COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'



class Participant:

    nr : int
    famList : List[float]
    targetList : List[str]
    blockShiftDict : dict



    def __init__(self, participantNr : int):
        self.nr = participantNr
        self.famList = Sequences.generate_famList(self.nr)
        #self.targetList = Sequences.generate_targetList()
        self.blockShiftDict = Participant.generate_blockShiftDict()

    def generate_blockShiftDict():
        blockShiftDict : dict = {}
        for i in range(Globals.N_BLOCKS):
            blockShiftDict[f"block{i}"] = Sequences.generate_nrSeq(Globals.N_SUBBLOCKS)
        return blockShiftDict

        





    def get_participantName(self) -> str:
        return "participant-{self.nr}"

    

    
       
        