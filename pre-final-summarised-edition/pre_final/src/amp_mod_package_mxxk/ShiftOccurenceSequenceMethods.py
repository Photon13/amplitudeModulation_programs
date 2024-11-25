import random
import numpy as np

from Globals import Globals

class ShiftOccurenceSequenceMethods:

    # for each block    
    # help method for generate_soundSequences()
    @staticmethod 
    def __assign_occurenceShift():
        n_subblocks = Globals.n_subblocks   
        # n_1secSnippets = n_subblocks * 4

        shiftOccurence = random.choices(["left", "middle", "right"], k= (n_subblocks-1))
        shiftOccurence = ["no"]+ shiftOccurence # 0. subblock no shift

        return shiftOccurence
    
    # for each block
    @staticmethod 
    def generate_soundSequences():
        shiftOccurence = ShiftOccurenceSequenceMethods.__assign_occurenceShift()
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
        
        nrSeqLeft = np.array(nrSeqLeft).astype('int32')
        # nrSeqLeft = np.append(0, nrSeqLeft) #?
        nrSeqMiddle = np.array(nrSeqMiddle).astype('int32')
        # nrSeqMiddle = np.append(0, nrSeqMiddle) #?
        nrSeqRight = np.array(nrSeqRight).astype('int32')
        # nrSeqRight = np.append(0, nrSeqRight) #?

        return shiftOccurence, nrSeqLeft, nrSeqMiddle, nrSeqRight