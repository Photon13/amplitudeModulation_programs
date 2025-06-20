from freefield import freefield
from pathlib import Path
import os

#from CommonHelpFunctions import CommonHelpFunctions #works
#from Fams import Fams #works
#from Dateien import Dateien #works
from Generator import Generator #works
#from Main import Main


#from Freifeld import Freifeld
#from Leds import Leds


#nrSeq = Generator.generate_nrSeq_withShifts(20, ampRiseValue = 7.0)
#print(nrSeq)
#print("Breakpoint")







"""
#_________________________________________________________________________

#testLeds: issue:
#Bits leuchten, aber Leds selbst nicht
# Digital I/O stecker drin auch schlecht, Leds sind dann permanent an (re,mi und oben)

#________________________________________________________________________

# !!!! MONKEY PATCH !!!! #
Freifeld.PATH_RCX = Path(os.getcwd()) /"data"/"rcx"/"V7.rcx" #_test
#Freifeld.PATH_RCX = Path(os.getcwd()) /"data"/"rcx"/"V7_test.rcx" #_test
  # does actually override Freifeld.PATH_RCX for the whole runtime (-> also the following Freifeld.init_FF() uses the patched value))
# !!!! MONKEY PATCH !!!! #

#bei V7_test.rcx blinkt bit 2 (bei nutzung rx81 oder rx82)
# bei V7_rcx blinken korrekte bits (bei nutzung rx81 oder rx82)

#________________________________________________________________________
"""