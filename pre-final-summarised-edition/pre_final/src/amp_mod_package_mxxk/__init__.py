# to do: 

# add a way to save participant instance as json

# decide which frequencies to use (cave: artefacts)
# find out whether 4 electrodes for eeg are enough

#__________
# holydays:

# create classes for preprocessing
# create classes for data analysis
    ## put each participant into dict
#__________
# christmas:

# fix leds:
    # to do: check if led coordinates are correct now
        ## maybe check if someone changed the freefield table ?

# check if sounds are properly played (just run __init__py)

# try out experiment with only buttons for a few blocks
    ## run BrainVision Recorder meanwhile
    ## skip while loop -> auto-continue after few seconds
        ### (because no one is at pc for input)
    ## check if button presses and zBus shown in 
    ## ggf. put 2 electrodes on frons and 1 ref on proc. mastoideus
        #### where to put the grounding?
    ## check if json is properly saved

# do that multiple times to get some "test" participants
    ## to try out preprocessing and data analysis
        ### multiple jsons and for each json one BrainVision Recorder 'measurement'

#___________
# to do: create flyer for advertisement participants
# to do: ask prof if psy students can get credit points
# send prof design to check if everything was understood correctly


import freefield
import slab

import numpy as np
from datetime import datetime
import time

import os
import sys
from pathlib import Path


from Globals import Globals
from ParticipantHelpMethods import ParticipantHelpMethods
from Participant import Participant
from Block import Block

from SoundMxxk import SoundMxxk
from SpeakerMethods import SpeakerMethods
from LedMethods import LedMethods

from ExportMethods import ExportMethods


np.set_printoptions(linewidth = 200)

class ExperimentWrapperMethods:
     
    def prepare_block(participant:Participant, block_nr): # works as desired
        participant.blockDict[f"block_{block_nr}"].set_shiftOccurence()
        participant.blockDict[f"block_{block_nr}"].set_nrSeqs()

        #print(participant.blockDict[f"block_{block_nr}"].shiftOccurence)
        return participant.blockDict[f"block_{block_nr}"]

    def run_block(participant:Participant, block_nr):
        SpeakerMethods.write_toSpeakers(participant, block_nr)
        LedMethods.turn_targetLed_on(participant, block_nr)
        freefield.play(kind='zBusA')
        # (block onset ("timepoint" zBus trigger) button press events
        # are directly sent to BrainVision Recorder)

        # wait:
        #stopTime = time.time() + 124 + 1   # 124 + 1 seconds from now
        stopTime = time.time() + 5 # for testing
        while True:
            if time.time() > stopTime:
                LedMethods.turn_all_leds_off()
                break

        





proc_list = [['RP2', 'RP2', Globals.path_cwd],
             ['RX81', 'RX8', Globals.path_cwd],
             ['RX82', 'RX8', Globals.path_cwd]]

freefield.initialize('dome', device=proc_list)

participant_nr = 55
# initiate participant:
participant = ParticipantHelpMethods.precreate_participant(participant_nr)
#ParticipantHelpMethods.export_participantInstance_asJson(participant, participant_nr)

# create sound snippets
soundData_list = SoundMxxk.set_soundSnippets(participant)

# initiate blocks of participant:
for i in range(Globals.N_BLOCKS):
     participant.blockDict[f"block_{i}"] = ExperimentWrapperMethods.prepare_block(i)

ExportMethods.export_participantInstance_asJson(participant)

for i in range(Globals.N_BLOCKS):
    print(f"\nRunning block_{i} ...")
    ExperimentWrapperMethods.run_block(i)
    print(f"block_{i} finished.")
    while True:
        inp = input("\nContinue with next block? [yes]/no: ")
        if inp.lower() == "yes":
            break


# export participant data as json !





    
    