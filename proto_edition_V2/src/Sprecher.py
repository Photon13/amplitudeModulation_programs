from Globals import Globals

import freefield

import sys

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

class Sprecher():


    @staticmethod
    def get_speakerCoordinates():

        [leftSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[0]) 
        [middleSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[1])
        [rightSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[2])

        return leftSpeaker, middleSpeaker, rightSpeaker



    @staticmethod
    def get_speaker(position : str) -> freefield.Speaker:
        if( position == "left"):
            n : int = 0
        elif( position == "middle"):
            n : int = 1
        elif( position == "right"):
            n : int = 2
        else:
            print( COLORRED + "CAVE: Invalid position! " + COLOREND + "Sprecher.get_speaker()")
            sys.exit()

        [sprecher] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[n]) #freefield.pick_speakers() always returns List[Speaker]!
        return sprecher                                                      # [x] = List[<>] unpacks List containing single value, i.e. x will be the entry of the List
    
    
    
    
    @staticmethod
    def write(position : str, nrSeq):
        sp = Sprecher.get_speaker(position)

        freefield.write("ampRise", 0.3, sp.analog_proc)
        freefield.write("n_snippets", len(nrSeq), sp.analog_proc)
        freefield.write(f"channel{position.capitalize()}", sp.analog_channel, sp.analog_proc)
        freefield.write(f"nrSeq{position.capitalize()}", nrSeq, sp.analog_proc)
