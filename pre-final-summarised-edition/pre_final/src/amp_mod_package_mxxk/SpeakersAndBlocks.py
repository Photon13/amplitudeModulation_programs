import random
from typing import List

import slab
import freefield

from Globals import Globals
from SoundsAndSequences import SoundsAndSequences


class SpeakersAndBlocks:

    def write_speakers(soundList, shiftOccurence):
                
        speakerCoordinates  = Globals.speakerCoordinates
        [speakerLeft] = freefield.pick_speakers( speakerCoordinates[0])
        [speakerMiddle] = freefield.pick_speakers( speakerCoordinates[1])
        [speakerRight] = freefield.pick_speakers( speakerCoordinates[2])

        freefield.write( "channelLeft", speakerLeft.analog_channel, speakerLeft.analog_proc)
        freefield.write( "channelMiddle", speakerMiddle.analog_channel, speakerMiddle.analog_proc)
        freefield.write( "channelRight", speakerRight.analog_channel, speakerRight.analog_proc)

        shiftOccurence, nrSeqLeft, nrSeqMiddle, nrSeqRight = SoundsAndSequences.generate_soundSequences()
        freefield.write( "nrSeqLeft", nrSeqLeft, speakerLeft.analog_proc )
        freefield.write( "nrSeqMiddle", nrSeqMiddle, speakerMiddle.analog_proc )
        freefield.write( "nrSeqRight", nrSeqRight, speakerRight.analog_proc )

        soundLeft_base = soundList[0]
        soundLeft_shifted = soundList[1]
        soundMiddle_base = soundList[2]
        soundMiddle_shifted = soundList[3]
        soundRight_base = soundList[4]
        soundRight_shifted = soundList[5]


        freefield.write( "baseLeft_n_samples", soundLeft_base.n_samples, speakerLeft.analog_proc)
        freefield.write( "baseMiddle_n_samples", soundMiddle_base.n_samples, speakerRight.analog_proc)
        freefield.write( "baseRight_n_samples", soundRight_base.n_samples, speakerRight.analog_proc)
        freefield.write( "shiftedLeft_n_samples", soundLeft_shifted.n_samples, speakerLeft.analog_proc)
        freefield.write( "shiftedMiddle_n_samples", soundMiddle_shifted.n_samples, speakerRight.analog_proc)
        freefield.write( "shiftedRight_n_samples", soundRight_shifted.n_samples, speakerRight.analog_proc)

        freefield.write( "baseLeft_data", soundLeft_base.data, speakerLeft.analog_proc)
        freefield.write( "baseMiddle_data", soundMiddle_base.data, speakerRight.analog_proc)
        freefield.write( "baseRight_data", soundRight_base.data, speakerRight.analog_proc)
        freefield.write( "shiftedLeft_data", soundLeft_shifted.data, speakerLeft.analog_proc)
        freefield.write( "shiftedMiddle_data", soundMiddle_shifted.data, speakerRight.analog_proc)
        freefield.write( "shiftedRight_data", soundRight_shifted.data, speakerRight.analog_proc)

        
        
        
        ### to add: n_trials



        return shiftOccurence



    # help method for generate_soundSnippets()
    @staticmethod
    def randomise_speakers(): 
        famUnshifted_list = Globals.famUnshifted_list # [famA_base, famB_base, famC_base]
        famShifted_list = Globals.famShifted_list # [famA_shifted, famB_shifted, famC_shifted]
        # Lists already include frequency values as int

        positions = random.sample(0,1,2, k=3) # randomise indices
        
        # assign frequencies to speakers:
        famLeft_base = famUnshifted_list[(positions[0])]
        famLeft_shifted = famShifted_list[(positions[0])]

        famMiddle_base = famUnshifted_list[(positions[1])]
        famMiddle_shifted = famShifted_list[(positions[1])] 

        famRight_base = famUnshifted_list[(positions[2])]
        famRight_shifted = famShifted_list[(positions[2])]  

        return famLeft_base, famLeft_shifted, famMiddle_base, famMiddle_shifted, famRight_base, famRight_shifted 
    
    @staticmethod
    def assign_targets():
        target_list = [(random.choice("left", "middle", "right"))]
        target_list = target_list + "both"

        random_targets = []
        random_targets = random_targets + "left" + "middle" + "right"+ "both"
        random_targets = random_targets + "left" + "middle" + "right"+ "both"
        random_targets = random_targets + "left" + "middle" + "right"+ "both"
        random_targets = random_targets + "left" + "middle" + "right"+ "both"

        random_targets = random.sample(random_targets, k=16) # randomise order
        target_list = target_list + random_targets

        return target_list
