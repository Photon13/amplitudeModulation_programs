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

COLORBLUE = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED = '\33[31m'
COLOREND = '\033[0m'




class Globals():

    #_______CONSTRUCTOR_of_GLOBALS____________________________________________________________________________________#

    def __init__(self, mode : str):
        """ mode == "testMode" 
            XOR
            mode == "non-testMode" """
        
        if(mode == "testMode"):
            print(COLORRED + "TESTMODE ENABLED" + COLOREND)

        if (mode == "testMode" or mode == "non-testMode"):
            self.mode = mode
        else: 
            (COLORRED + "Invalid mode! -> change mode in Globals() to \"testMode\" or \"non-testMode\"" + COLOREND)
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
    PATH_CWD = Path( os.getcwd() )
                                        #   amplitudeModulation / amplitudeModulation_programs / proto_edition_V1
                                        #   cwd must be: proto_edition_V1 !



    # Python files:
    PATH_PYTHON = PATH_CWD /"src"
                                        #   proto_edition_V1 / src

    
    
    # Rcx files:
    PATH_RCX_FILE = PATH_CWD /"data"/"rcx"/"standard_setup_long_pre_final.rcx"
                                        #   proto_edition_V1 / data / rcx / standard_setup_long_pre_final.rcx

    



    # Json txt:
    def get_pathJsonFolder(self) -> Path:
        pathJsonFolder : Path = Globals.PATH_CWD / "participant_json" / f"{self.mode}"
        return pathJsonFolder
                                        #   proto_edition_V1 / participant_json / <mode> / participant-{nr}.txt
                                        #   <mode> == testMode || non-testMode



    # Prime numbers:
        # proto_edition_V1 / data / possible_frequency_combinations.txt




    # BrainVision Recorder
    PATH_FOLDER_BRAINVISION_RECORDER = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder")
                                        
                                        #   amplitudeModulation / BrainVision Recorder / <mode>
                                        #   <mode> == testMode || non-testMode


    def get_pathBVR_rohDatenFolder(self) -> Path:         
        path_roh : Path = Globals.PATH_FOLDER_BRAINVISION_RECORDER / f"{self.mode}" / "rohDaten"
        return path_roh
                                        #   .eeg, .vhdr, .vmrk
                                        #   file name: e.g. participant-{}.eeg 
                                        #                   participant-{}(1).eeg

    def get_pathBVR_zwischenDatenFolder(self) -> Path:         
        path_zwischen : Path = Globals.PATH_FOLDER_BRAINVISION_RECORDER / f"{self.mode}" / "zwischenDaten"
        return path_zwischen
                                        #   preprocessed EEG (e.g. after interpolation)
                                        #   file name: e.g. participant-{}_zwischen.<> ?
    
    def get_pathBVR_vollVerarbeiteteDaten(self) -> Path:         
        path_voll : Path = Globals.PATH_FOLDER_BRAINVISION_RECORDER / f"{self.mode}" / "vollVerarbeiteteDaten"
        return path_voll
                                        #   e.g. diagrams
                                        #   file name: e.g. participant-{}_diagram_ABC_left_target
                                        #                   participant-{}_diagram_ABC_both_target

    #                 ------rohDaten
    #                       ------ participant-{}_roh
    #                              >>>>>> participant-{}.eeg
    #                              >>>>>> participant-{}(1).eeg
    #                              >>>>>> participant-{}.vhdr
    #                              >>>>>> participant-{}.vmrk
    #                 ------zwischenDaten
    #                       ------ participant-{}_zwischen
    #                 ------vollVerarbeiteteDaten
    #                       ------ summation
    #                              >>>>>> summation_diagram_ABC_left_target
    #                       ------ participant-{}_voll
    #                              ------ participant-{}_diagramme
    #                                     >>>>>> participant-{}_diagram_ABC_left_target




    



    

    


    



    def get_pathBVR_rohDaten_participantFolder(participantNr : int) -> Path:
        path_roh_part = Globals.get_pathBVR_rohDatenFolder() / "participant-{participantNr}_roh"
        return path_roh_part

    def get_pathBVR_zwischenDatenFolder_participantFolder(self, participantNr : int) -> Path:
        path_zwischen_part : Path = self.get_pathBVR_zwischenDatenFolder() / "participant-{participantNr}_zwischen"
        return path_zwischen_part

    def get_pathBVR_vollVerarbeiteteDaten_participantFolder(self, participantNr : int) -> Path:
        path_voll_part : Path = self.get_pathBVR_vollVerarbeiteteDaten() / "participant-{participantNr}_voll"
        return path_voll_part
    


    
    def get_pathBVR_vollVerarbeiteteDaten_summationFolder(self) -> Path:
        path_sum : Path = self.get_pathBVR_vollVerarbeiteteDaten() / "summation"
        return path_sum
            # diagrams: (?)
            #       - power spectrum:
            #               - powerSpektrum_leftTarget_{}Hz
            #               - powerSpektrum_leftTarget_{}Hz
            #               - powerSpektrum_leftTarget_{}Hz
            #
            #               - powerSpektrum_rightTarget_{}Hz
            #               - ...
            #
            # resultBVR.text (?)
            #       - Δpower_lateralTarget_single
            #       - Δpower_middleTarget_single
            #       - Δpower_lateralTarget_both
            #       - Δpower_middleTarget_both
            #
            # resultButtonPresses.txt (?)


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
    





        