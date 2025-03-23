import freefield
import slab
import random
import sys
import time
import numpy as np


from Sprecher import Sprecher
from Globals import Globals
from Experiment import Experiment


COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'




class TestMethods:
    """ Contains methods to be tested in main """

    @staticmethod
    def genRandom_shiftOccurence(positions : str, n_subblocks : int = 0) -> list[str]:
        """ enter EITHER n_subblocks or testDauer [sec], 
            leave the other one as 0
            CAVE: if testDauer is not multiple of 4, then the remaining rest will be deleted"""
        
        
        shiftOccurence : list[str] = ["none"] # 0.subblock
        possShiftPositions : list[str] = positions

        for i in range(1, n_subblocks):
            newEntry : str = random.choice(possShiftPositions)
            shiftOccurence.append(newEntry)

        return shiftOccurence





    def gen_rowNrs(position: str, n_subblocks) -> list[str]:
        """ generates sequence of equal numbers,
            number of numbers is 4*n_subblocks """
        rowNrs : list[str] = []

        if( position == "left" ):
            nr : int = 1
  
        elif( position == "middle" ):
            nr : int = 3

        elif( position == "right" ):
            nr : int = 5

        else:
            print(COLORRED + "Invalid position!" + COLOREND + "TestMethods.gen_rowNrs()")
            sys.exit()

        for i in range(0, n_subblocks):
            for i in range(0,4):
                rowNrs.append(nr)
        print(rowNrs)
        return rowNrs
    

    def replaceNrs_regularShift_basedOnTarget(rowNrs : list[str], shiftOccurrence : list[str], irregularShift : bool):
        """ takes number list and replaces a nr with an even nr, if a shift occurs"""

        if( irregularShift == False):
            addList : list[int] = [0, 0, 0]             # shift occurs always in 1st second of subblock

        elif( irregularShift == True):
            addList : list[int] = [0, 1, 2]             # shift occurrs in resp. 1st, 2nd XOR 3rd second of subblock
        
        if( rowNrs[0] == 1 ): # i.e. left speaker
                                                        # index in nrSeq (rowNrs) must be quadruple of index in shiftOcurrence (in case of 1st entry = 1)
            for i in range(0, len(shiftOccurrence)):     # index-reduction undone, then the index quadruplicated, then index lowered by 1 again
                x : int = random.choice(addList)            #     
                if( shiftOccurrence[i] == "left"):       # then new entry = old entry + 1; to make even nr out of odd nr (e.g. 3 -> 4 for middle speaker)    
                    rowNrs[(i*4)+x] += 1                # then add x [sec], if shift shall occur irregularly          
                                                                                                          
        elif( rowNrs[0] == 3 ): # i.e. middle speaker

            for i in range(0, len(shiftOccurrence)):
                x : int = random.choice(addList)
                if( shiftOccurrence[i] == "middle"):
                    rowNrs[(i*4)+x] += 1
        
        elif( rowNrs[0] == 5 ): # i.e. right speaker

            for i in range(0, len(shiftOccurrence)):
                x : int = random.choice(addList)
                if( shiftOccurrence[i] == "right"):
                    rowNrs[(i*4)+x] += 1

        else:
            print(COLORRED + "Invalid rowNrs!" + COLOREND + "TestMethods.replaceNrs_basedOnTarget()")
            sys.exit()

        return rowNrs


    def convert_rowNrs_to_nrSeq(rowNrs : list[str]):
        nrSeq = np.array(rowNrs).astype('int32')
        return nrSeq
    

    def wrapper_gen_nrSeqs(position: str, n_subblocks, shiftOccurence : list[str], irregularShift : bool = False):
        rowNrsRoh : list[str] = TestMethods.gen_rowNrs(position, n_subblocks)
        rowNrsReplac = TestMethods.replaceNrs_regularShift_basedOnTarget(rowNrsRoh, shiftOccurence, irregularShift)
        nrSeq = TestMethods.convert_rowNrs_to_nrSeq(rowNrsReplac)
        return nrSeq




    @staticmethod
    def test_speakers(positions : list[str], frequencies : list[int], shift : bool = False, irregularShift : bool = False, n_subblocks : int = 0):
        """ enter all speaker positions to be tested simultaneously
                e.g. ["left", "middle"] 
            enter all frequencies in same order
                e.g. [13, 17]                   """
        
        leftSpeaker, middleSpeaker, rightSpeaker = Sprecher.get_speakerCoordinates()

        if( len(positions) != len(frequencies)):
            print( COLORRED + "Frequencies must have same number of entries as positions!" 
                            + COLOREND + "TestMethods.test_pureAMpinknoise()")
            sys.exit()
        
        
        if( shift == True):
            shiftOccurrence = TestMethods.genRandom_shiftOccurence(positions, n_subblocks)
        else:
            shiftOccurrence : list[str] = []
            for i in range(0, n_subblocks):
                shiftOccurrence.append("none")

        duration    : float = Globals.DURATION
        samplerate  : int = Globals.SAMPLERATE
        level       : int = Globals.LEVEL

        leftSpeaker, middleSpeaker, rightSpeaker = Sprecher.get_speakerCoordinates()

        for i in range(0, len(positions)):  # loops through all given speakers

            speakerPosition : str     =  positions[i]
            freq            : int     =  frequencies[i]

            pinknoise         =  slab.Sound.pinknoise( duration = duration, samplerate = samplerate, level = level )
            pinknoiseAM       =  pinknoise.am(freq)

            nrSeq =  TestMethods.wrapper_gen_nrSeqs( speakerPosition, n_subblocks, shiftOccurrence, irregularShift )
            n_snippets      : int     =  len(nrSeq)


            if( speakerPosition == "left"):

                freefield.write( "channelLeft",             leftSpeaker.analog_channel,     leftSpeaker.analog_proc )
                freefield.write( "nrSeqLeft",               nrSeq,                          leftSpeaker.analog_proc )
                freefield.write( "n_snippetsLeft",          n_snippets,                     leftSpeaker.analog_proc )
                freefield.write( "shiftedLeft_n_samples",   pinknoiseAM.n_samples,          leftSpeaker.analog_proc )
                freefield.write( "baseLeft_n_samples",      pinknoiseAM.n_samples,          leftSpeaker.analog_proc )
                freefield.write( "baseLeft_data",           pinknoiseAM.data,               leftSpeaker.analog_proc )
                freefield.write( "shiftedLeft_data",        pinknoiseAM.data,               leftSpeaker.analog_proc )


            elif( speakerPosition == "middle"):

                freefield.write( "channelMiddle",           middleSpeaker.analog_channel,   middleSpeaker.analog_proc )
                freefield.write( "nrSeqMiddle",             nrSeq,                          middleSpeaker.analog_proc )
                freefield.write( "n_snippetsMiddle",        n_snippets,                     middleSpeaker.analog_proc )
                freefield.write( "shiftedMiddle_n_samples", pinknoiseAM.n_samples,          middleSpeaker.analog_proc )
                freefield.write( "baseMiddle_n_samples",    pinknoiseAM.n_samples,          middleSpeaker.analog_proc )
                freefield.write( "baseMiddle_data",         pinknoiseAM.data,               middleSpeaker.analog_proc )
                freefield.write( "shiftedMiddle_data",      pinknoiseAM.data,               middleSpeaker.analog_proc )


            elif( speakerPosition == "right"):

                freefield.write( "channelRight",            rightSpeaker.analog_channel,    rightSpeaker.analog_proc )   
                freefield.write( "nrSeqRight",              nrSeq,                          rightSpeaker.analog_proc )
                freefield.write( "n_snippetsRight",         n_snippets,                     rightSpeaker.analog_proc )
                freefield.write( "shiftedRight_n_samples",  pinknoiseAM.n_samples,          rightSpeaker.analog_proc )
                freefield.write( "baseRight_n_samples",     pinknoiseAM.n_samples,          rightSpeaker.analog_proc )
                freefield.write( "baseRight_data",          pinknoiseAM.data,               rightSpeaker.analog_proc )
                freefield.write( "shiftedRight_data",       pinknoiseAM.data,               rightSpeaker.analog_proc )

            freefield.play()
            print("Trigger sent")

            print(f"nrSeq: {nrSeq}")
            print(f"shiftOccurrence: {shiftOccurrence}")
            print(f"n_subblocks: {n_subblocks}")
    
    


