import os
from pathlib import Path


class Paths:

    PATH_CWD : Path = Path( os.getcwd() )
    #PATH_RCX : Path = PATH_CWD /"data"/"rcx"/"V5_pilot.rcx"
    PATH_RCX : Path = PATH_CWD /"V5_pilot.rcx"

    #PATH_JSON_FOLDER = PATH_CWD / "participant_json" / Settings.MODE

    PATH_FOLDER_BRAINVISION_RECORDER : Path = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder")


    def get_fileName_jsonParticipant(participantNr : int) -> Path:
        return Path(Paths.PATH_JSON_FOLDER /f"participant-{participantNr}.txt")