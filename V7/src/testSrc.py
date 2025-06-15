from freefield import freefield
from pathlib import Path
import os

#from CommonHelpFunctions import CommonHelpFunctions #works
#from Fams import Fams #works
from Dateien import Dateien #works
from Generator import Generator #works
from Main import Main


from Freifeld import Freifeld
#from Leds import Leds


#________________________________________________________________________

# !!!! MONKEY PATCH !!!! #
Freifeld.PATH_RCX = Path(os.getcwd()) /"data"/"rcx"/"V7_test.rcx" #_test
  # does actually override Freifeld.PATH_RCX for the whole runtime (-> also the following Freifeld.init_FF() uses the patched value))
# !!!! MONKEY PATCH !!!! #


Freifeld.init_FF()

#Freifeld.turnTargetLedOn("left")

Freifeld.writeToSpeaker("left", 33.3, [0.3,0.4,0.5,0.0]) #?
#Freifeld.writeToSpeaker("left", 30.0, Generator.generateListOfZeros(10))
#freefield.play()



#_________________________________________________________________________

#testLeds: issue:
#Bits leuchten, aber Leds selbst nicht
# Digital I/O stecker drin auch schlecht, Leds sind dann permanent an (re,mi und oben)

#_______________________________________________________________________


"""
Exception has occurred: AttributeError
'NoneType' object has no attribute 'SetTagVal'
  File "C:\projects\Maik_R_F_K\Biologie Bachelor\Bachelorarbeit\amplitudeModulation\amplitudeModulation_programs\V7\src\Freifeld.py", line 44, in writeToSpeaker
    freefield.write( f"channel{position.capitalize()}",    speaker.analog_channel,             speaker.analog_proc )
  File "C:\projects\Maik_R_F_K\Biologie Bachelor\Bachelorarbeit\amplitudeModulation\amplitudeModulation_programs\V7\src\testSrc.py", line 24, in <module>
    Freifeld.writeToSpeaker("left", 30.0, Generator.generateListOfZeros(10))
AttributeError: 'NoneType' object has no attribute 'SetTagVal'
"""
