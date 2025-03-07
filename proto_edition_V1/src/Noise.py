import slab
import random
import numpy as np

from Globals import Globals

COLORBLUE = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED = '\33[31m'
COLOREND = '\033[0m'




class Noise:

    @staticmethod # only at start
    def generate_soundSnippets(participant : object) -> dict: # seems to work (?)
        
        famLeft_base = participant.famDict["famLeft_base"]
        famMiddle_base = participant.famDict["famMiddle_base"]
        famRight_base = participant.famDict["famRight_base"]

        famLeft_shifted = participant.famDict["famLeft_shifted"]
        famMiddle_shifted = participant.famDict["famMiddle_shifted"]
        famRight_shifted = participant.famDict["famRight_shifted"]

        samplerate = 48828
        level = 75
        duration = 1.0 # float!

        pinknoise = slab.Sound.pinknoise( duration = duration, samplerate = samplerate, level = level)

        soundLeft_base = pinknoise.am( frequency = famLeft_base)
        soundLeft_shifted = pinknoise.am( frequency = famLeft_shifted)

        soundMiddle_base = pinknoise.am( frequency = famMiddle_base)
        soundMiddle_shifted = pinknoise.am( frequency = famMiddle_shifted)

        soundRight_base = pinknoise.am( frequency = famRight_base)
        soundRight_shifted = pinknoise.am( frequency = famRight_shifted)
        
        # fade-in #CAVE: USELESS, ramp must occur in first snippet not all snippets!!!
        #soundLeft_base.ramp(when ='onset', duration = 1.0)
        #soundLeft_shifted.ramp(when = 'onset', duration = 1.00)

        #soundMiddle_base.ramp(when = 'onset', duration = 1.00)
        #soundMiddle_shifted.ramp(when = 'onset', duration = 1.00)

        #soundRight_base.ramp(when = 'onset', duration = 1.00)
        #soundRight_shifted.ramp(when = 'onset', duration = 1.00)


        dictSoundData = {
                "soundLeft_base": soundLeft_base,
                "soundLeft_shifted": soundLeft_shifted,
                "soundMiddle_base": soundMiddle_base,
                "soundMiddle_shifted": soundMiddle_shifted,
                "soundRight_base": soundRight_base,
                "soundRight_shifted": soundRight_shifted}

        return dictSoundData




    @staticmethod # for each block
    def generate_nrSeqs(participant : object, blockNr : int) -> dict:
        """ Help method for write_nrSeqs(participant, leftSpeaker, middleSpeaker, rightSpeaker) 
        
            Creates lists containing numbers for each position: 
                left no shift:   1  ;  left shift:   2
                middle no shift: 3  ;  middle shift: 4
                right no shift:  5  ;  right shift:  6       """
        
        shiftOccurence : list[str] = participant.blockShiftDict[f"block_{blockNr}"]
            # n_subblocks

        # 0. subblock (no shift at all):
        nrSeqLeft = [1,1,1,1]
        nrSeqMiddle = [3,3,3,3]
        nrSeqRight = [5,5,5,5]

        
        # other subblocks:
        for i in range( 1, len(shiftOccurence) ): # 0. entry skipped

            if( shiftOccurence[i] == "l" ):
                nrSeqLeft = nrSeqLeft + [2,1,1,1] # shift
                nrSeqMiddle = nrSeqMiddle + [3,3,3,3] # no shift
                nrSeqRight = nrSeqRight + [5,5,5,5] # no shift

            elif( shiftOccurence[i] == "m" ):
                nrSeqLeft = nrSeqLeft + [1,1,1,1] # no shift
                nrSeqMiddle = nrSeqMiddle + [4,3,3,3] # shift
                nrSeqRight = nrSeqRight + [5,5,5,5] # no shift

            elif( shiftOccurence[i] == "r" ):
                nrSeqLeft = nrSeqLeft + [1,1,1,1] # no shift
                nrSeqMiddle = nrSeqMiddle + [3,3,3,3] # no shift
                nrSeqRight = nrSeqRight + [6,5,5,5] # shift

            else: 
                print(COLORRED + "\nProblem occured in generate_nrSeqs(): Probably invalid target in shiftOccurence list." + COLOREND)


        nrSeqLeft = np.array(nrSeqLeft).astype('int32') # nrSeqLeft = np.append(0, nrSeqLeft) #?
        nrSeqMiddle = np.array(nrSeqMiddle).astype('int32')  # nrSeqMiddle = np.append(0, nrSeqMiddle) #?
        nrSeqRight = np.array(nrSeqRight).astype('int32') # nrSeqRight = np.append(0, nrSeqRight) #?

        #nrSeqLeft = np.append(0, nrSeqLeft)
        #nrSeqMiddle = np.append(0, nrSeqMiddle)
        #nrSeqRight = np.append(0, nrSeqRight)
    	
        nrSeqsDict : dict = {}
        nrSeqsDict["nrSeqLeft"] = nrSeqLeft
        nrSeqsDict["nrSeqMiddle"] = nrSeqMiddle
        nrSeqsDict["nrSeqRight"] = nrSeqRight


        print(COLORGREEN + "Sounds successfully prepared. " + COLOREND + "Message from generate_soundSnippets(participant : object)")
        return nrSeqsDict