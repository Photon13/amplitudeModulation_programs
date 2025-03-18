from datetime import *

from Globals import Globals

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

class Log_data:

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
    
     
    def write_to_dateienLog(text : str):

        path_dateienLog = Globals.get_pathDateienLog()
        
        with open(path_dateienLog, "a") as f:           #append!
            date : str = Log_data.get_currentDate()
            zeit : str = Log_data.get_currentTime()
            f.write(date + " " + zeit + " ")
            f.write(text + "\n")