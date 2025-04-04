from Dateien import Dateien
from Experiment import Experiment
from Globals import Globals
from Led import Led
from Participant import Participant
from Paths import Paths
from Sequences import Sequences
from Settings import Settings
from Sprecher import Sprecher
from Tests import Tests

import freefield

import numpy as np




COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

np.set_printoptions(linewidth = 200)


        #   Python: Settings: "non-testMode"
        # Rcx: Load rcx onto procs (->)
        # Brainvison Recorder: Start in eye mode (Auge)
        #   Python: Run Tests

        # Brainvision: Start recording
        # Brainvision: File name: Maik_DD_MM_YYYY
        #   Python : Run Experiment






if __name__ == "__main__":

                # Python: Settings: "non-testMode" / "testMode"
                # Rcx: Load rcx onto procs (->)
                # Brainvison Recorder: Start in eye mode (Auge)

    proc_list = [['RP2', 'RP2', Paths.PATH_RCX],
                ['RX81', 'RX8', Paths.PATH_RCX],
                ['RX82', 'RX8', Paths.PATH_RCX]]

    freefield.initialize('dome', device=proc_list)

    #_____TEST_______________________________________________________
    
    Tests.test_threeSpeakers(n_subblocks = 14, freqs = [0.0, 0.0, 0.0], shift = False)
        #Lautstärke messen

                # Python: Run Tests
    
    #Led.test_allLeds()
    #Tests.test_threeSpeakers(n_subblocks = 12, freqs = Globals.FAM_LIST, shift = True)
    #Tests.test_singleSpeaker("right", n_subblocks, 4.7, True)


    #_____EXPERIMENT_______________________________________________________
    
                # Brainvision: Start recording
                # Brainvision: File name: Maik_DD_MM_YYYY
                # Python : Run Experiment

    while True:
        inp = input("Start Experiment? [yes]: ")
        if( inp.lower() == "yes"):
            break

    participant = Participant(1)
    #run block loop

    














