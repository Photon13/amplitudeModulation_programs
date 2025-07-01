from Globals import Globals
from Participant import Participant
from Sprecher import Sprecher
from Led import Led

import numpy as np


COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)




class Experiment:

    @staticmethod
    def run_block(participant : Participant, blockNr : int): # CAVE: procs must have been initiated first!
        
        Led.turnOn_targetLed_forTimeIntervall()
        print(COLORGREEN + "Target LED turned on" + COLOREND)

        Sprecher.writeToAndTrigger_speakers(Globals.POSITIONEN, 
                                            participant.famList,
                                            participant.blockShiftDict[f"block{blockNr}"])
        print(COLORGREEN + "Data wrote to speakers." + COLOREND)
        print(COLORGREEN + "Trigger sent." + COLOREND)


    #@staticmethod
    #def runBlockLoop(blockToStartWith : int):

    #@staticmethod
    #def continueExperiment():
        # participantNr = Dateien.get_lastParticipantNr()
        # 
        # read blockToStartWith from Json
        # if block done -> withe to part json log
    
    #@staticmethod
    #def start_newExperiment():
        # participantNr = Dateien.generate_nextParticipantNr()






