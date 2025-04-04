from datetime import *

from Globals import Globals
from Paths import Paths

from pathlib import Path

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'



class Logs:

    @staticmethod
    def get_currentDate() -> str:
        currentDate : date = date.today()
        currentDate : str = currentDate.strftime( '%Y-%m-%d' )
        return currentDate
    
    @staticmethod
    def get_currentTime() -> str:
        currentDateTime : datetime = datetime.now()
        currentTime : str = currentDateTime.strftime( '%H:%M' )
        return currentTime
    
    @staticmethod
    def writeTo_log(text : str, pathLog : Path):
        with open(pathLog, "a") as f:           #append!
            date : str = Logs.get_currentDate()
            zeit : str = Logs.get_currentTime()
            f.write(date + " " + zeit + " ")
            f.write(text + "\n")



    @staticmethod
    def writeTo_logAllParticipants(text : str):
        pathLog = Paths.PATH_CWD / "participant_json" / "logs" / "dateienLog.txt"
        Logs.writeTo_log(text, pathLog)

    @staticmethod
    def writeTo_participantSpecificLog(participantNr : int, text : str):
        pathLog = Paths.PATH_CWD / "participant_json" / "logs" / f"logParticipant{participantNr}.txt"
        Logs.writeTo_log(text, pathLog)



    @staticmethod
    def writeToLog_blockDone(participantNr : int, blockNr : int):
        Logs.writeTo_participantSpecificLog(participantNr, f"Block{blockNr} finished. ")

    @staticmethod
    def writeToLog_participantCreated(participantNr : int):
        Logs.writeTo_logAllParticipants(f"Participant{participantNr} created. ")
    
    @staticmethod
    def writeToLog_participantreinitiated(participantNr : int, nrNextBlock : int):
        Logs.writeTo_logAllParticipants(f"Participant{participantNr} reinitiated. New run started with block{nrNextBlock} ")