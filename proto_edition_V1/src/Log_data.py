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

    def write_to_dateienLog():

        path_dateienLog = Globals.PATH_CWD
        #with open(path_dateienLog, "w") as f: