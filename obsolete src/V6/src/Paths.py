import os
from pathlib import Path


class Paths:

    PATH_CWD : Path = Path( os.getcwd() )
    PATH_RCX : Path = PATH_CWD /"data"/"rcx"/"V6.rcx"

    # Save copies:
    #PATH_FOLDER_BRAINVISION_RECORDER : Path = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder")
    
    PATH_FOLDER_BRAINVISION_RECORDER_PRETEST : Path = PATH_CWD /"BrainVision Recorder files"/"EEG Marker Files PreTest"
    PATH_FOLDER_BRAINVISION_RECORDER_MAINEXP : Path = PATH_CWD /"BrainVision Recorder files"/"EEG Main Exp"
    PATH_FOLDER_JSON : Path = PATH_CWD/"json"