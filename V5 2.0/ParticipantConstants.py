from Globals import Globals

class ParticipantConstants:


    #FOLLOWING VALUES NOT TO BE CHANGED:
    FAM_LIST_0 = Globals.FAM_LIST
    FAM_LIST_1 = [Globals.FAM_A, Globals.FAM_C, Globals.FAM_B] 
    FAM_LIST_2 = [Globals.FAM_C, Globals.FAM_A, Globals.FAM_B] 
    FAM_LIST_3 = [Globals.FAM_C, Globals.FAM_B, Globals.FAM_A] 
    FAM_LIST_4 = [Globals.FAM_B, Globals.FAM_A, Globals.FAM_C] 
    FAM_LIST_01234 = [FAM_LIST_0, FAM_LIST_1, FAM_LIST_2, FAM_LIST_3, FAM_LIST_4]

    TARGET_LIST_0 = ['middle', 'left', 'right', 'both', 'both', 'left', 'both', 'both', 'right', 'both', 'left', 'right', 'right', 'left', 'middle', 'left', 'middle', 'right', 'middle', 'middle']
    TARGET_LIST_1 = ['right', 'left', 'middle', 'both', 'left', 'left', 'left', 'middle', 'right', 'right', 'right', 'right', 'both', 'middle', 'both', 'both', 'middle', 'left', 'both', 'middle']
    TARGET_LIST_2 = ['right', 'middle', 'left', 'both', 'right', 'both', 'middle', 'both', 'left', 'both', 'both', 'left', 'right', 'middle', 'left', 'middle', 'right', 'middle', 'right', 'left']
    TARGET_LIST_3 = ['left', 'right', 'middle', 'both', 'both', 'middle', 'both', 'left', 'left', 'middle', 'both', 'right', 'left', 'middle', 'right', 'middle', 'right', 'left', 'both', 'right']
    TARGET_LIST_4 = ['middle', 'right', 'left', 'both', 'left', 'right', 'middle', 'both', 'right', 'left', 'middle', 'right', 'middle', 'left', 'both', 'middle', 'both', 'both', 'right', 'left']
    TARGET_LIST_01234 = [TARGET_LIST_0, TARGET_LIST_1, TARGET_LIST_2, TARGET_LIST_3, TARGET_LIST_4]
    #______
 

    @staticmethod
    def get_famList(participantNr):
        if participantNr in [0,1,2,3,4]:
            return ParticipantConstants.FAM_LIST_01234[participantNr]
        else:
            return ParticipantConstants.FAM_LIST_01234[0]
        
    @staticmethod
    def get_targetList(participantNr):
        if participantNr in [0,1,2,3,4]:
            return ParticipantConstants.TARGET_LIST_01234[participantNr]
        else:
            return ParticipantConstants.TARGET_LIST_01234[0]