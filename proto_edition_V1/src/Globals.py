#_______good frequency combinations_________#:
#
#
#
#
#
#
#
#
#
#



import os
from pathlib import Path
import re
import sys

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'




class Globals:

    #_______CONSTRUCTOR_of_GLOBALS____________________________________________________________________________________#

    def __init__(self, mode : str):
        """ modes: "testMode", "non-testMode" """

        if (mode == "testMode" or mode == "non-testMode"):
            self.mode = mode

            if(mode == "testMode"):
                print("    " +COLORPURPLE + "TEST mode enabled" + COLOREND)
            else:
                print("    " + COLORPURPLE + "NORMAL mode enabled" + COLOREND)
        else: 
            (COLORRED + "Invalid mode! Change mode in Globals() to \"testMode\" or \"non-testMode\"" + COLOREND)
            sys.exit()


    #_______ COORDINATES: ____________________________________________________________________________________________#

    # Coordinates for horizontal speakers:                  
    #    (-52.5, 0)                                         
    #    (-35.5, 0)                                         
    #    (-17.5, 0)
    #    (0, 0) 
    #    (17.5) 
    #    (35.5, 0) 
    #    (52.5, 0)

    LED_COORDINATES = [(0, -25), (0, 0), (0, 25)]
    SPEAKER_COORDINATES = [(-35, 0), (0, 0), (35, 0)]
    


    #_______ FREQUENCIES: ___________________________________________________#

    # Frequencies of Amplitude modulation___:
    FAM_A_BASE = 3
    FAM_B_BASE = 7
    FAM_C_BASE = 13

    # ΔFrequency___:
    SHIFT_A = 4
    SHIFT_B = SHIFT_A
    SHIFT_C = SHIFT_A

    # Shift is added to base fam________:
    FAM_A_SHIFTED = FAM_A_BASE + SHIFT_A
    FAM_B_SHIFTED = FAM_B_BASE + SHIFT_B
    FAM_C_SHIFTED = FAM_C_BASE + SHIFT_C
    
    FAM_ABC_BASE_LIST =     [FAM_A_BASE, FAM_B_BASE, FAM_C_BASE]
    FAM_ABC_SHIFTED_LIST =  [FAM_A_SHIFTED, FAM_B_SHIFTED, FAM_C_SHIFTED]
    SHIFT_ABC_LIST =        [SHIFT_A, SHIFT_B, SHIFT_C]
    

    #_______BLOCKS_and_SUBBLOCKS_____________________________________________#

    # Number of subblocks___:           ##### CAVE: SUBBLOCK LASTS 2 SECONDS FOR WHATEVER REASON!
    N_SUBBLOCKS = (1+15)   
                                        #   16 subblocks, 4 seconds resp.
                                        #   1st second: shifted sound; 2.-4. second: unshifted sound 
                                        #   in sum: 1 block = 64 seconds (4 sec * 31)
                                        #   CAVE: 0.subblock: always unshifted ! 

    # Number of blocks___:   
    N_BLOCKS = (2+16)       
                                        #   2 test blocks + 16 normal blocks
                                        #   4 conditions (i.e. target types)), 4 blocks resp.


    #_______SOUND___________________________________________________________#

    SAMPLERATE : int = 48828
    LEVEL : int = 75
    DURATION : float= 1.0 # float!

    #_______PATHS___________________________________________________________#

    # Path cwd:
    PATH_CWD : Path = Path( os.getcwd() )
                                        #   amplitudeModulation / amplitudeModulation_programs / proto_edition_V1
                                        #   cwd must be: proto_edition_V1 !

    # Python files:
    PATH_PYTHON : Path = PATH_CWD /"src"
                                        #   proto_edition_V1 / src
    
    # Rcx files:
    PATH_RCX_FILE : Path = PATH_CWD /"data"/"rcx"/"standard_setup_long_pre_final.rcx"
                                        #   proto_edition_V1 / data / rcx / standard_setup_long_pre_final.rcx


    # Json txt:
    @staticmethod
    def get_pathJsonFolder(mode : str) -> Path:
        return Globals.PATH_CWD / "participant_json" / f"{mode}"

                                        #   proto_edition_V1 / participant_json / <mode> / participant-{nr}.txt
                                        #   <mode> == testMode || non-testMode

    # Log files:
    @staticmethod
    def get_pathDateienLog() -> Path:
        return Globals.PATH_CWD / "participant_json" / "logs" / "dateienLog.txt"


    # BrainVision Recorder
    PATH_FOLDER_BRAINVISION_RECORDER : Path = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder")
                                        
                                        #   amplitudeModulation / BrainVision Recorder / <mode>
                                        #   <mode> == testMode || non-testMode

    @staticmethod
    def get_pathBVR_rohDatenFolder(mode : str) -> Path:         
        return Globals.PATH_FOLDER_BRAINVISION_RECORDER / f"{mode}" / "rohDaten"
                                        #   .eeg, .vhdr, .vmrk
                                        #   file name: e.g. participant-{}.eeg 
                                        #                   participant-{}(1).eeg


    @staticmethod
    def get_searchPatternDict(participantNr : int) -> dict:

        SEARCH_PATTERN_eeg = re.compile( rf"participant-  {participantNr}  \.  eeg", re.VERBOSE)
        SEARCH_PATTERN_eeg_additionalFiles = re.compile( rf"participant-  {participantNr}  [(] \d+ [)]  \.  eeg", re.VERBOSE)

        SEARCH_PATTERN_vhdr = re.compile( rf"participant-  {participantNr}  \.  vhdr", re.VERBOSE)
        SEARCH_PATTERN_vhdr_additionalFiles = re.compile( rf"participant-  {participantNr}  [(] \d+ [)]  \.  vhdr", re.VERBOSE)

        SEARCH_PATTERN_vmrk = re.compile( rf"participant-  {participantNr}  \.  vmrk", re.VERBOSE)
        SEARCH_PATTERN_vmrk_additionalFiles = re.compile( rf"participant-  {participantNr}  [(] \d+ [)]  \.  vmrk", re.VERBOSE)


        searchPatternDict : dict = {
            "SEARCH_PATTERN_eeg" : SEARCH_PATTERN_eeg,
            "SEARCH_PATTERN_eeg_additionalFiles" : SEARCH_PATTERN_eeg_additionalFiles,
            "SEARCH_PATTERN_vhdr" : SEARCH_PATTERN_vhdr,
            "SEARCH_PATTERN_vhdr_additionalFiles" : SEARCH_PATTERN_vhdr_additionalFiles,
            "SEARCH_PATTERN_vmrk" : SEARCH_PATTERN_vmrk,
            "SEARCH_PATTERN_vmrk_additionalFiles" : SEARCH_PATTERN_vmrk_additionalFiles
        }
        return searchPatternDict
    





        