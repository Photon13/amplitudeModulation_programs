import os
from pathlib import Path

class Globals():
    
    path_cwd = Path(os.getcwd())
    # folder .../amplitudeModulation_programs/pre-final-summarised-edition has to be opened !

    ledCoordinates = [(0, -25), (0, 0), (0, 25)]
    speakerCoordnates = [(-37.5, 0), (0, 0), (37.5, 0)]

    
    famA_base = 7
    famB_base = 9
    famC_base = 11
    famUnshifted_list = [famA_base, famB_base, famC_base]

    shift = 6
    famA_shifted = famA_base + shift
    famB_shifted = famB_base + shift
    famC_shifted = famC_base + shift
    famShifted_list = [famA_shifted, famB_shifted, famC_shifted]

    n_blocks=16 # final ! -> bei Änderung muss SoundsAndSequences.assign_targets() angepasst werden
    n_subblocks = 5