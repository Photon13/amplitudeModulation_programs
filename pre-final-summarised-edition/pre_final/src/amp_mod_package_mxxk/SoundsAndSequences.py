import random

import slab
import freefield

from Globals import Globals
from typing import List

#_______________________________________________________________________________________________________________________

class SoundsAndSequences:

    """ at start of experiment"""
    @staticmethod
    def generate_soundSnippets():
        famLeft_base, famLeft_shifted, famMiddle_base, famMiddle_shifted, famRight_base, famRight_shifted = SoundsAndSequences.randomise_speakers()

        samplerate = 48828
        level = 80
        duration = 1.0 # float!

        pinknoise = slab.pinknoise( duration= duration, samplerate= samplerate, level= level)

        soundLeft_base = pinknoise.am( frequency= famLeft_base)
        soundLeft_shifted = pinknoise.am( frequency= famLeft_shifted)

        soundMiddle_base = pinknoise.am( frequency= famMiddle_base)
        soundMiddle_shifted = pinknoise.am( frequency= famMiddle_shifted)

        soundRight_base = pinknoise.am( frequency= famRight_base)
        soundRight_shifted = pinknoise.am( frequency= famRight_shifted)

        soundList = [soundLeft_base, soundLeft_shifted, soundMiddle_base, soundMiddle_shifted, soundRight_base, soundRight_shifted]

        return soundList
    
    #_______________________________________________________________________________________________________________________

    # help method for generate_soundSequences()
    @staticmethod 
    def assign_occurenceShift():
        n_subblocks = Globals.n_subblocks   
        # n_1secSnippets = n_subblocks * 4

        shiftOccurence = random.choices(["left", "middle", "right"], k= (n_subblocks-1))
        shiftOccurence = ["no"]+ shiftOccurence # 0. subblock no shift

        return shiftOccurence
    
    """" for each block"""
    @staticmethod 
    def generate_soundSequences():
        shiftOccurence = SoundsAndSequences.assign_occurenceShift()
        """
        left no shift:   1  ;  left shift:   2
        middle no shift: 3  ;  middle shift: 4
        right no shift:  5  ;  right shift:  6
        """
        # 0. subblock:
        nrSeqLeft = [1,1,1,1]
        nrSeqMiddle = [3,3,3,3]
        nrSeqRight = [5,5,5,5]

        # other subblocks:
        for index in range( 1, len(shiftOccurence) ): # 0. entry skipped
            if( shiftOccurence[index] == "left" ):
                nrSeqLeft = nrSeqLeft + [1,1,1,1] # target
                nrSeqMiddle = nrSeqMiddle + [4,4,4,4] # non-target
                nrSeqRight = nrSeqRight + [6,6,6,6] # non-target
            elif( shiftOccurence[index] == "middle" ):
                nrSeqLeft = nrSeqLeft + [2,2,2,2] # non-target
                nrSeqMiddle = nrSeqMiddle + [3,3,3,3] # target
                nrSeqRight = nrSeqRight + [6,6,6,6] # non-target

            elif( shiftOccurence[index] == "right" ):
                nrSeqLeft = nrSeqLeft + [2,2,2,2] # non-target
                nrSeqMiddle = nrSeqMiddle + [4,4,4,4] # non-target
                nrSeqRight = nrSeqRight + [5,5,5,5] # target
            else: 
                print("\nCAVE: nrSeq couldn't be generated.")

        #print(f"\n{nrSeqLeft}")
        #print(f"\n{nrSeqMiddle}")
        #print(f"\n{nrSeqRight}")
        #print(shiftOccurence)
        return shiftOccurence, nrSeqLeft, nrSeqMiddle, nrSeqRight
    #_______________________________________________________________________________________________________________________
