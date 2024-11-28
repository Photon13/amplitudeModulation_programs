# ADD n_trials IN write_speakers 

import random
import numpy as np

import freefield

from Globals import Globals
import SoundMethods
from ShiftOccurenceSequenceMethods import ShiftOccurenceSequenceMethods

class SpeakerMethods:

    # for each block
    @staticmethod
    def write_speakers(soundList):

        """ write the speaker coordinates on tag 'channel{position}' """
        speakerCoordinates  = Globals.speakerCoordinates
        [speakerLeft] = freefield.pick_speakers( speakerCoordinates[0])
        [speakerMiddle] = freefield.pick_speakers( speakerCoordinates[1])
        [speakerRight] = freefield.pick_speakers( speakerCoordinates[2])

        freefield.write( "channelLeft", speakerLeft.analog_channel, speakerLeft.analog_proc)
        freefield.write( "channelMiddle", speakerMiddle.analog_channel, speakerMiddle.analog_proc)
        freefield.write( "channelRight", speakerRight.analog_channel, speakerRight.analog_proc)


        """ generate number sequences and sounds
        -> odd numbers indicate an unshifted sound snippet (=base) shall be played
        -> even numbers indicate a shifted sound snippet shall be played
        each sound snippet is 1 sec long """
        shiftOccurence, nrSeqLeft, nrSeqMiddle, nrSeqRight = ShiftOccurenceSequenceMethods.generate_soundSequences()
        soundLeft_base = soundList[0] # soundList = [soundLeft_base, soundLeft_shifted, soundMiddle_base, soundMiddle_shifted, soundRight_base, soundRight_shifted]
        soundLeft_shifted = soundList[1]
        soundMiddle_base = soundList[2]
        soundMiddle_shifted = soundList[3]
        soundRight_base = soundList[4]
        soundRight_shifted = soundList[5]

        """ write an int[] containing numbers 
        (1 or 2) for left,  (3 or 4) for middle,  and (5 or 6) for right 
        onto tag 'nrSeq{position}' """
        freefield.write( "nrSeqLeft", nrSeqLeft, speakerLeft.analog_proc )
        freefield.write( "nrSeqMiddle", nrSeqMiddle, speakerMiddle.analog_proc )
        freefield.write( "nrSeqRight", nrSeqRight, speakerRight.analog_proc )

        """ write number of samples onto tag 'nrSeq{position}' """
        freefield.write( "baseLeft_n_samples", soundLeft_base.n_samples, speakerLeft.analog_proc)
        freefield.write( "baseMiddle_n_samples", soundMiddle_base.n_samples, speakerRight.analog_proc)
        freefield.write( "baseRight_n_samples", soundRight_base.n_samples, speakerRight.analog_proc)
        freefield.write( "shiftedLeft_n_samples", soundLeft_shifted.n_samples, speakerLeft.analog_proc)
        freefield.write( "shiftedMiddle_n_samples", soundMiddle_shifted.n_samples, speakerRight.analog_proc)
        freefield.write( "shiftedRight_n_samples", soundRight_shifted.n_samples, speakerRight.analog_proc)
        
        """ write int[] containing sound data onto tag '{sound type}{position}_data' """
        freefield.write( "baseLeft_data", soundLeft_base.data, speakerLeft.analog_proc)
        freefield.write( "baseMiddle_data", soundMiddle_base.data, speakerRight.analog_proc)
        freefield.write( "baseRight_data", soundRight_base.data, speakerRight.analog_proc)
        freefield.write( "shiftedLeft_data", soundLeft_shifted.data, speakerLeft.analog_proc)
        freefield.write( "shiftedMiddle_data", soundMiddle_shifted.data, speakerRight.analog_proc)
        freefield.write( "shiftedRight_data", soundRight_shifted.data, speakerRight.analog_proc)

        """ write number of respective trials (= number of respective 1sec sound snippets) onto tag 'n_snippets{position}'"""
        # n_1sec_snippets = n_4sec_subblocks * 4
        n_snippets = (Globals.n_subblocks * 4) # number of 1 sec snippets i.e. sounds loaded
        freefield.write("n_snippets_Left", n_snippets, speakerLeft.analog_proc)
        freefield.write("n_snippets_Middle", n_snippets, speakerMiddle.analog_proc)
        freefield.write("n_snippets_Right", n_snippets, speakerRight.analog_proc)


        return shiftOccurence
    
    # only at start experiment
    # help method for generate_soundSnippets()
    @staticmethod
    def randomise_speakers(): # works as desired
        famUnshifted_list = Globals.famUnshifted_list # [famA_base, famB_base, famC_base]
        famShifted_list = Globals.famShifted_list # [famA_shifted, famB_shifted, famC_shifted]
        # Lists already include frequency values as int

        positions = np.random.shuffle(0,1,2) # randomise order
        
        # assign frequencies to speakers:
        famLeft_base = famUnshifted_list[(positions[0])] # position[0] may be integer 0 XOR 1 XOR 2
        famLeft_shifted = famShifted_list[(positions[0])]

        famMiddle_base = famUnshifted_list[(positions[1])] # position[1] may be integer 0 XOR 1 XOR 2
        famMiddle_shifted = famShifted_list[(positions[1])] 

        famRight_base = famUnshifted_list[(positions[2])] # position[2] may be integer 0 XOR 1 XOR 2
        famRight_shifted = famShifted_list[(positions[2])]  

        print(f"\nfamLeft_base = {famLeft_base} Hz, famMiddle_base = {famMiddle_base} Hz, famRight_base = {famRight_base} Hz")

        return famLeft_base, famLeft_shifted, famMiddle_base, famMiddle_shifted, famRight_base, famRight_shifted
    
    