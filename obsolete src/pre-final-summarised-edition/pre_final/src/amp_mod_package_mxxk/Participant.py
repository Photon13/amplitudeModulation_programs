import random
from typing import List
import json

from Globals import Globals
from Block import Block


   
class Participant:

    name: str
    date: str
    famLMR_base_list: List[int]
    famLMR_shifted_list: List[int]
    N_BLOCKS: int
    N_SUBBLOCKS: int

    #block_{}.target: str
    #block_{}.shiftOccurence: List[str]
    #block_{}.nrSeq{}: numpy.array[int32]

    @staticmethod # help method for __init__()
    def load_json(participant_nr): 
        load_path = Globals.get_path_json1(participant_nr)
        with open( load_path, 'r') as file:
            dict = json.load(file)
        return dict

    def __init__(self, participant_nr): 
        dict = Participant.load_json(participant_nr)
        for key in dict:
            setattr(self, key, dict[key])
        #print(self.__dict__)
        print("{")
        for key, value in self.__dict__.items():
            print(f"{key} : {value}")
        print("}")
    
    # n_participants = <...>
    # for i in range( n_participants)
    #   participant_nr = i
    #   participant_i = Participant(participant_nr)


"""
BEFORE EXPERIMENT STARTS:

participant_nr = <...>
ParticipantHelpMethods.precreate_participant(participant_nr)
ParticipantHelpMethods.export_participantInstance_asJson(participant: ParticipantHelpMethods)


"""
"""
AFTER ALL EXPERIMENTS ARE DONE:

participant_nr = <...>
Participant.load_json()
participant_<...> = Participant(participant_nr)
"""




