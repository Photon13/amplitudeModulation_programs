import os
from pathlib import Path


class Paths:

    PATH_CWD : Path = Path( os.getcwd() )
    PATH_RCX : Path = PATH_CWD /"data"/"rcx"/"V6.rcx"

    # Save copies:
    #PATH_FOLDER_BRAINVISION_RECORDER : Path = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder")
    
    PATH_FOLDER_BRAINVISION_RECORDER : Path = PATH_CWD /"BrainVision Recorder files"/"EEG Recordings"
    PATH_FOLDER_JSON : Path = PATH_CWD/"json"