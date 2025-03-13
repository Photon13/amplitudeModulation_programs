import freefield
import slab
import random
import sys
import time
import numpy as np


from Sprecher import Sprecher
from Globals import Globals


COLORBLUE = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED = '\33[31m'
COLOREND = '\033[0m'




class TestMethods:
    """ Contains methods to be tested in main """

    @staticmethod
    def genRandom_shiftOccurence(testDauer : int = 0, n_subblocks : int = 0) -> list[str]:
        """ enter EITHER n_subblocks or testDauer [sec], 
            leave the other one as 0
            CAVE: if testDauer is not multiple of 4, then the remaining rest will be deleted"""
        
        if(testDauer > 0 and n_subblocks == 0):
            n_oneSecSnippets : int = int(testDauer / 4) # rest is deleted if not multiple of 4
            if(testDauer%4 != 0):
                print(COLORRED + "CAVE: testDauer was not multiple of 4, therefore play time is reduced (by max. 3 secs)" + COLOREND)

        elif( testDauer == 0 and n_subblocks >0):
            n_oneSecSnippets : int = n_subblocks
        else:
            print(COLORRED + "Invalid parameters!" + COLORBLUE + "Enter EITHER n_subblocks or testDauer as params, the other one must be 0 or left out")
            sys.exit()

        shiftOccurence : list[str] = []
        possShiftPositions : list[str] = ["left", "middle", "right"]
        for i in range(0, n_oneSecSnippets):
            newEntry : str = random.choice(possShiftPositions)
            shiftOccurence.append(newEntry)

        return shiftOccurence



    @staticmethod
    def test_pureAMpinknoise(positions : list[str], frequencies : list[int], shiftOccurence : list[str]):
        """ enter all speaker positions to be tested simultaneausly
                e.g. ["left", "middle"] 
            enter all frequencies in same order
                e.g. [13, 17]                   """
        
        
        if( len(positions) != len(frequencies)):
            print( COLORRED + "frequencies must have same number of entries as positions!" 
                            + COLOREND + "TestMethods.test_pureAMpinknoise()")
            sys.exit()
        
        duration    : int = Globals.DURATION, 
        samplerate  : int = Globals.SAMPLERATE, 
        level       : int = Globals.LEVEL
        

        for i in range(0, len(positions)):  # loops through all given speakers

            speakerPosition : str     =  positions[i]
            freq            : int     =  frequencies[i]

            speaker         : object  =  Sprecher.getSpeaker(speakerPosition)

            pinknoise       : object  =  slab.Sound.pinknoise( duration, samplerate, level )
            pinknoiseAM     : object  =  pinknoise.am(freq)

            nrSeq                     =  TestMethods.wrapper_gen_nrSeqs( speakerPosition, 
                                                                         len(shiftOccurence), 
                                                                         shiftOccurence )
            n_snippets      : int     =  len(nrSeq)


            if( speakerPosition == "left"):

                freefield.write( "channelLeft",             speaker.analog_channel,     speaker.analog_proc )
                freefield.write( "nrSeqLeft",               nrSeq,                      speaker.analog_proc )
                freefield.write( "n_snippetsLeft",          n_snippets,                 speaker.analog_proc )
                freefield.write( "shiftedLeft_n_samples",   pinknoiseAM.n_samples,      speaker.analog_proc )
                freefield.write( "baseLeft_n_samples",      pinknoiseAM.n_samples,      speaker.analog_proc )
                freefield.write( "baseLeft_data",           pinknoiseAM.data,           speaker.analog_proc )
                freefield.write( "shiftedLeft_data",        pinknoiseAM.data,           speaker.analog_proc )


            elif( speakerPosition == "middle"):

                freefield.write( "channelMiddle",           speaker.analog_channel,     speaker.analog_proc )
                freefield.write( "nrSeqMiddle",             nrSeq,                      speaker.analog_proc )
                freefield.write( "n_snippetsMiddle",        n_snippets,                 speaker.analog_proc )
                freefield.write( "shiftedMiddle_n_samples", pinknoiseAM.n_samples,      speaker.analog_proc )
                freefield.write( "baseMiddle_n_samples",    pinknoiseAM.n_samples,      speaker.analog_proc )
                freefield.write( "baseMiddle_data",         pinknoiseAM.data,           speaker.analog_proc )
                freefield.write( "shiftedMiddle_data",      pinknoiseAM.data,           speaker.analog_proc )


            elif( speakerPosition == "right"):

                freefield.write( "channelRight",            speaker.analog_channel,     speaker.analog_proc )   
                freefield.write( "nrSeqRight",              nrSeq,                      speaker.analog_proc )
                freefield.write( "n_snippetsRight",         n_snippets,                 speaker.analog_proc )
                freefield.write( "shiftedRight_n_samples",  pinknoiseAM.n_samples,      speaker.analog_proc )
                freefield.write( "baseRight_n_samples",     pinknoiseAM.n_samples,      speaker.analog_proc )
                freefield.write( "baseRight_data",          pinknoiseAM.data,           speaker.analog_proc )
                freefield.write( "shiftedRight_data",       pinknoiseAM.data,           speaker.analog_proc )




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

        return rowNrs
    

    def replaceNrs_basedOnTarget(rowNrs : list[str], shiftOccurence : list[str]):
        """ takes number list and replaces a nr with an even nr, if a shift occurs"""
        
        if( rowNrs[0] == 1 ): # i.e. left speaker
                                                        # the index in nrSeq (rowNrs) must be the quadruple of the index in shiftOcurrence (in case of 1st entry = 1)
            for i in range(0, len(shiftOccurence)):     # index-reduction is undone, then the index is quadruplicated, then index lowered by 1 again     
                if( shiftOccurence[i] == "left"):       # this way, we get the correct index of the nr in rowNrs, which we want to change       
                    rowNrs[((i+1)*4)-1] += 1            # then we change the entry by adding 1, to make an even nr out of an odd nr (e.g. 3 -> 4 for middle speaker)     
                                                                                                          
        elif( rowNrs[0] == 3 ): # i.e. middle speaker

            for i in range(0, len(shiftOccurence)):
                if( shiftOccurence[i] == "middle"):
                    rowNrs[((i+1)*4)-1] += 1
        
        elif( rowNrs[0] == 5 ): # i.e. right speaker

            for i in range(0, len(shiftOccurence)):
                if( shiftOccurence[i] == "right"):
                    rowNrs[((i+1)*4)-1] += 1

        else:
            print(COLORRED + "Invalid rowNrs!" + COLOREND + "TestMethods.replaceNrs_basedOnTarget()")
            sys.exit()

        return rowNrs


    def convert_rowNrs_to_nrSeq(rowNrs : list[str]):
        nrSeq = np.array(rowNrs).astype('int32')
        return nrSeq
    

    def wrapper_gen_nrSeqs(position: str, n_subblocks, shiftOccurence : list[str]):
        rowNrsRoh : list[str] = TestMethods.gen_rowNrs(position , n_subblocks)
        rowNrsReplac = TestMethods.replaceNrs_basedOnTarget(rowNrsRoh, shiftOccurence)
        nrSeq = TestMethods.convert_rowNrs_to_nrSeq(rowNrsReplac)
        return nrSeq
    
    


