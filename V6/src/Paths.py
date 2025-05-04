import os
from pathlib import Path


class Paths:

    PATH_CWD : Path = Path( os.getcwd() )
    PATH_RCX : Path = PATH_CWD /"data"/"rcx"/"V6.rcx"

    PATH_FOLDER_BRAINVISION_RECORDER : Path = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder")

