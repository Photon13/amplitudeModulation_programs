import os
import json

from Globals import Globals

class ParticipantList:

    def __init__():
        search_path = Globals.path_participantInfo
        fileList = [ file 
                     for file in os.listdir(search_path) # list of all files in participant information folder
                     if os.isfile( os.join(search_path, file) )
                    ]
        substring = "info_1"
        json1_list = [  file 
                        for file in fileList
                        if substring in file ]
        print(json1_list)
        
        """
        for i in range(0, json1_list.len()):
            load_path = Globals.path_participantInfo / f"{json1_list[i]}"

        load_path = Globals.get_path_json1(participant_nr)
        with open( load_path, 'r') as file:

        dict = json.load(file)
        for key in dict:
            setattr(self, key, dict[key])
        """
participantList = ParticipantList()