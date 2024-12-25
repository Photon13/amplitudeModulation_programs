import freefield
import random
import sys
from Participant import Participant
from Noise import Noise
from Led import Led
from Sprecher import Sprecher
from Globals import Globals

COLORBLUE = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED = '\33[31m'
COLOREND = '\033[0m'

class TestMethods:

    @staticmethod
    def init_processors():

        proc_list = [['RP2', 'RP2', Globals.PATH_RCX_FILE],
                    ['RX81', 'RX8', Globals.PATH_RCX_FILE],
                    ['RX82', 'RX8', Globals.PATH_RCX_FILE]]

        freefield.initialize('dome', device=proc_list)



    @staticmethod
    def wrapper_participantPreparation(participantNr : int):
        participant = Participant(participantNr)
        participant.export_participantInstance_toJson()
        print(COLORGREEN + "Participant information successfully prepared. " + COLOREND + "Message from wrapper_participantPreparation(participantNr : int))")


    @staticmethod
    def run_block(participant : object, blockNr : int, dictSoundData : dict):
        target : str = participant.targetList[blockNr]
        #Led.turn_targetLed_on(target)
        Sprecher.wrapper_writeTo_speakers(participant, blockNr, dictSoundData)