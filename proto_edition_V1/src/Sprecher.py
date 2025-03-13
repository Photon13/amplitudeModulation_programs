import freefield
import slab
import sys

from Globals import Globals
from Noise import Noise

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLOREND = '\033[0m'




class Sprecher():

    @staticmethod
    def getSpeaker(position : str) -> object:
        """ returns speaker object by calling it from coordinates from Globals"""

        if( position == "left"):
            [leftSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[0]) 
            return leftSpeaker
        
        elif( position == "middle"):
            [middleSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[1])
            return middleSpeaker
        
        elif( position == "right"):
            [rightSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[2])
            return rightSpeaker
        
        else:
            print(COLORRED + "Invalid position!" + COLOREND + "Sprecher.getSpeaker()")
            sys.exit()


    @staticmethod
    def get_speakerCoordinates():

        [leftSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[0]) 
        [middleSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[1])
        [rightSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[2])

        return leftSpeaker, middleSpeaker, rightSpeaker
    


    @staticmethod
    def write_channel(leftSpeaker, middleSpeaker, rightSpeaker) -> None:

        freefield.write("channelLeft", leftSpeaker.analog_channel, leftSpeaker.analog_proc)
        freefield.write("channelMiddle", middleSpeaker.analog_channel, middleSpeaker.analog_proc)
        freefield.write("channelRight", rightSpeaker.analog_channel, rightSpeaker.analog_proc)
    



    @staticmethod
    def write_nrSeqs(participant : object, blockNr : int,
                     leftSpeaker : object, middleSpeaker : object, rightSpeaker : object ) -> None:
        """  #   send sequence of number onto rcx:
             #       for left: 1 (= no shift) or 2 (= shift), resp.;
             #       for left: 3 (= no shift) or 4 (= shift), resp.;
             #       for left: 5 (= no shift) or 6 (= shift), resp.    """

        nrSeqsDict = Noise.generate_nrSeqs(participant, blockNr)
        print(nrSeqsDict)

        freefield.write( "nrSeqLeft",   nrSeqsDict["nrSeqLeft"],   leftSpeaker.analog_proc   )
        freefield.write( "nrSeqMiddle", nrSeqsDict["nrSeqMiddle"], middleSpeaker.analog_proc )
        freefield.write( "nrSeqRight",  nrSeqsDict["nrSeqRight"],  rightSpeaker.analog_proc )
 
    



    @staticmethod
    def write_nSnippets(participant : object, leftSpeaker : object, middleSpeaker : object, rightSpeaker : object) -> None:

        freefield.write( "n_snippetsLeft",   (participant.n_subblocks *4), leftSpeaker.analog_proc   ) 
        freefield.write( "n_snippetsMiddle", (participant.n_subblocks *4), middleSpeaker.analog_proc )
        freefield.write( "n_snippetsRight",  (participant.n_subblocks *4), rightSpeaker.analog_proc  )
    



    @staticmethod
    def write_nSamples(dictSoundData : dict,
                             leftSpeaker : object, middleSpeaker : object, rightSpeaker : object) -> None:
        
        freefield.write( "shiftedLeft_n_samples",   dictSoundData["soundLeft_shifted"].n_samples,   leftSpeaker.analog_proc   )
        freefield.write( "shiftedMiddle_n_samples", dictSoundData["soundMiddle_shifted"].n_samples, middleSpeaker.analog_proc )
        freefield.write( "shiftedRight_n_samples",  dictSoundData["soundRight_shifted"].n_samples,  rightSpeaker.analog_proc  )

        freefield.write( "baseLeft_n_samples",   dictSoundData["soundLeft_base"].n_samples,   leftSpeaker.analog_proc   )
        freefield.write( "baseMiddle_n_samples", dictSoundData["soundMiddle_base"].n_samples, middleSpeaker.analog_proc )
        freefield.write( "baseRight_n_samples",  dictSoundData["soundRight_base"].n_samples,  rightSpeaker.analog_proc  )
    
 


    @staticmethod
    def write_soundData(dictSoundData : dict, 
                        leftSpeaker : object, middleSpeaker : object, rightSpeaker : object ) -> None:
        """ send sound data (data per snippet type) onto rcx """
        
        freefield.write( "baseLeft_data",   dictSoundData["soundLeft_base"].data,   leftSpeaker.analog_proc   )
        freefield.write( "baseMiddle_data", dictSoundData["soundMiddle_base"].data, middleSpeaker.analog_proc )
        freefield.write( "baseRight_data",  dictSoundData["soundRight_base"].data,  rightSpeaker.analog_proc  )

        freefield.write( "shiftedLeft_data",   dictSoundData["soundLeft_shifted"].data,   leftSpeaker.analog_proc   )
        freefield.write( "shiftedMiddle_data", dictSoundData["soundMiddle_shifted"].data, middleSpeaker.analog_proc )
        freefield.write( "shiftedRight_data",  dictSoundData["soundRight_shifted"].data,  rightSpeaker.analog_proc  )




    @staticmethod
    def wrapper_writeTo_speakers(participant : object, blockNr : int, dictSoundData : dict):

        print(COLORGREEN + "Writing to speakers ... " + COLOREND)
        leftSpeaker, middleSpeaker, rightSpeaker = Sprecher.get_speakerCoordinates()
        
        Sprecher.write_channel( 
            leftSpeaker, middleSpeaker, rightSpeaker
        )
        Sprecher.write_nrSeqs(  
            participant, blockNr,
            leftSpeaker, middleSpeaker, rightSpeaker 
        )
        Sprecher.write_nSnippets( 
            participant,  
            leftSpeaker, middleSpeaker, rightSpeaker
        )
        Sprecher.write_nSamples(  
            dictSoundData,
            leftSpeaker, middleSpeaker, rightSpeaker
        )
        Sprecher.write_soundData(   
            dictSoundData, 
            leftSpeaker, middleSpeaker, rightSpeaker 
        )   




""" # ['RX81', 'RX82'] funzt nicht:

    @staticmethod
    def write_channel(leftSpeaker, middleSpeaker, rightSpeaker) -> None:

        freefield.write("channelLeft", leftSpeaker.analog_channel, ['RX81', 'RX82'])
        freefield.write("channelMiddle", middleSpeaker.analog_channel, ['RX81', 'RX82'])
        freefield.write("channelRight", rightSpeaker.analog_channel, ['RX81', 'RX82'])
    

    @staticmethod
    def write_nrSeqs(participant : object, blockNr : int,
                     leftSpeaker : object, middleSpeaker : object, rightSpeaker : object ) -> None:

        nrSeqsDict = Noise.generate_nrSeqs(participant, blockNr)

        freefield.write( "nrSeqLeft",   nrSeqsDict["nrSeqLeft"],   ['RX81', 'RX82']   )
        freefield.write( "nrSeqMiddle", nrSeqsDict["nrSeqMiddle"], ['RX81', 'RX82'] )
        freefield.write( "nrSeqRight",  nrSeqsDict["nrSeqRight"],  ['RX81', 'RX82'] )
            # send sequence of number onto rcx:
            #   for left: 1 (= no shift) or 2 (= shift), resp.;
            #   for left: 3 (= no shift) or 4 (= shift), resp.;
            #   for left: 5 (= no shift) or 6 (= shift), resp. 
    

    @staticmethod
    def write_nSnippets(participant : object, leftSpeaker : object, middleSpeaker : object, rightSpeaker : object) -> None:

        freefield.write( "n_snippetsLeft",   (participant.n_subblocks *4), ['RX81', 'RX82']   ) # 16 * 4
        freefield.write( "n_snippetsMiddle", (participant.n_subblocks *4), ['RX81', 'RX82'] )
        freefield.write( "n_snippetsRight",  (participant.n_subblocks *4), ['RX81', 'RX82']  )
    

    @staticmethod
    def write_nSamples(dictSoundData : dict,
                             leftSpeaker : object, middleSpeaker : object, rightSpeaker : object) -> None:
        
        freefield.write( "shiftedLeft_n_samples",   dictSoundData["soundLeft_shifted"].n_samples,   ['RX81', 'RX82']   )
        freefield.write( "shiftedMiddle_n_samples", dictSoundData["soundMiddle_shifted"].n_samples, ['RX81', 'RX82'] )
        freefield.write( "shiftedRight_n_samples",  dictSoundData["soundRight_shifted"].n_samples,  ['RX81', 'RX82']  )
    
    
    @staticmethod
    def write_soundData(dictSoundData : dict, 
                        leftSpeaker : object, middleSpeaker : object, rightSpeaker : object ) -> None:

        # send sound data (data per snippet type) onto rcx
        freefield.write( "baseLeft_data",   dictSoundData["soundLeft_base"].data,   ['RX81', 'RX82']   )
        freefield.write( "baseMiddle_data", dictSoundData["soundMiddle_base"].data, ['RX81', 'RX82'] )
        freefield.write( "baseRight_data",  dictSoundData["soundRight_base"].data,  ['RX81', 'RX82']  )

        freefield.write( "shiftedLeft_data",   dictSoundData["soundLeft_shifted"].data,   ['RX81', 'RX82']   )
        freefield.write( "shiftedMiddle_data", dictSoundData["soundMiddle_shifted"].data, ['RX81', 'RX82'] )
        freefield.write( "shiftedRight_data",  dictSoundData["soundRight_shifted"].data,  ['RX81', 'RX82']  )
"""




    

    
