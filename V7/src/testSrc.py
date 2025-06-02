from freefield import freefield

#from CommonHelpFunctions import CommonHelpFunctions #works
#from Dateien import Dateien #works
#from Fams import Fams #works
from Generator import Generator #works


from Freifeld import Freifeld
#from Leds import Leds
#from Main import Main


#testLeds: issue:
#Bits leuchten, aber Leds selbst nicht
# Digital I/O stecker drin auch schlecht, Leds sind dann permanent an (re,mi und oben)

#print(Generator.generate_valuesInRange([0,2], 5))

#x="tag"
#print(f"hello world{x}".capitalize())

Freifeld.init_FF()
Freifeld.writeToSpeaker("left", 30.0, Generator.generateListOfZeros(10))
freefield.play()
"""
Exception has occurred: AttributeError
'NoneType' object has no attribute 'SetTagVal'
  File "C:\projects\Maik_R_F_K\Biologie Bachelor\Bachelorarbeit\amplitudeModulation\amplitudeModulation_programs\V7\src\Freifeld.py", line 44, in writeToSpeaker
    freefield.write( f"channel{position.capitalize()}",    speaker.analog_channel,             speaker.analog_proc )
  File "C:\projects\Maik_R_F_K\Biologie Bachelor\Bachelorarbeit\amplitudeModulation\amplitudeModulation_programs\V7\src\testSrc.py", line 24, in <module>
    Freifeld.writeToSpeaker("left", 30.0, Generator.generateListOfZeros(10))
AttributeError: 'NoneType' object has no attribute 'SetTagVal'
"""
"""
print(speakerCoordinates)
print(speaker.analog_channel)
print(speaker.analog_proc)
print(f"channel{position.capitalize()}")
(-35, 0)
1
RX82
channelLeft
"""