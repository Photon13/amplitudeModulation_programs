import freefield

from Globals import Globals
from Noise import Noise

COLORBLUE = '\33[34m'
COLORRED = '\33[31m'
COLOREND = '\033[0m'

class Sprecher():

    #@staticmethod
    def get_speakerCoordinates():

        #freefield.read_speaker_table()
        #SPEAKER_COORDINATES = [0, 1, 2]
        [leftSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[0]) 
        [middleSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[1])
        [rightSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[2])

        """
        [leftSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[0]) 
        [middleSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[1])
        [rightSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[2])
        """
        return leftSpeaker, middleSpeaker, rightSpeaker
    

    @staticmethod
    def write_channel(leftSpeaker, middleSpeaker, rightSpeaker) -> None:

        freefield.write("channelLeft", leftSpeaker.analog_channel, leftSpeaker.analog_proc)
        freefield.write("channelMiddle", middleSpeaker.analog_channel, middleSpeaker.analog_proc)
        freefield.write("channelRight", rightSpeaker.analog_channel, rightSpeaker.analog_proc)
    

    @staticmethod
    def write_nrSeqs(participant : object, blockNr : int,
                     leftSpeaker : object, middleSpeaker : object, rightSpeaker : object ) -> None:

        nrSeqsDict = Noise.generate_nrSeqs(participant, blockNr)

        freefield.write( "nrSeqLeft",   nrSeqsDict["nrSeqLeft"],   leftSpeaker.analog_proc   )
        freefield.write( "nrSeqMiddle", nrSeqsDict["nrSeqMiddle"], middleSpeaker.analog_proc )
        freefield.write( "nrSeqRight",  nrSeqsDict["nrSeqRight"],  rightSpeaker.analog_proc )
            # send sequence of number onto rcx:
            #   for left: 1 (= no shift) or 2 (= shift), resp.;
            #   for left: 3 (= no shift) or 4 (= shift), resp.;
            #   for left: 5 (= no shift) or 6 (= shift), resp. 
    

    @staticmethod
    def write_nSnippets(leftSpeaker : object, middleSpeaker : object, rightSpeaker : object) -> None:

        freefield.write( "n_snippetsLeft",   (Globals.N_SUBBLOCKS *4), leftSpeaker.analog_proc   )
        freefield.write( "n_snippetsMiddle", (Globals.N_SUBBLOCKS *4), middleSpeaker.analog_proc )
        freefield.write( "n_snippetsRight",  (Globals.N_SUBBLOCKS *4), rightSpeaker.analog_proc  )
    

    @staticmethod
    def write_nSoundSnippets(dictSoundData : dict,
                             leftSpeaker : object, middleSpeaker : object, rightSpeaker : object) -> None:
        
        freefield.write( "shiftedLeft_n_samples",   dictSoundData["soundLeft_shifted"].n_samples,   leftSpeaker.analog_proc   )
        freefield.write( "shiftedMiddle_n_samples", dictSoundData["soundMiddle_shifted"].n_samples, middleSpeaker.analog_proc )
        freefield.write( "shiftedRight_n_samples",  dictSoundData["soundRight_shifted"].n_samples,  rightSpeaker.analog_proc  )
    
    
    @staticmethod
    def write_soundData(dictSoundData : dict, 
                        leftSpeaker : object, middleSpeaker : object, rightSpeaker : object ) -> None:

        # send sound data (data per snippet type) onto rcx
        freefield.write( "baseLeft_data",   dictSoundData["soundLeft_base"].data,   leftSpeaker.analog_proc   )
        freefield.write( "baseMiddle_data", dictSoundData["soundMiddle_base"].data, middleSpeaker.analog_proc )
        freefield.write( "baseRight_data",  dictSoundData["soundRight_base"].data,  rightSpeaker.analog_proc  )

        freefield.write( "shiftedLeft_data",   dictSoundData["soundLeft_shifted"].data,   leftSpeaker.analog_proc   )
        freefield.write( "shiftedMiddle_data", dictSoundData["soundMiddle_shifted"].data, middleSpeaker.analog_proc )
        freefield.write( "shiftedRight_data",  dictSoundData["soundRight_shifted"].data,  rightSpeaker.analog_proc  )

    @staticmethod
    def wrapper_writeTo_speakers(participant : object, blockNr : int, dictSoundData : dict):

        leftSpeaker, middleSpeaker, rightSpeaker = Sprecher.get_speakerCoordinates()
        
        Sprecher.write_channel( 
            leftSpeaker, middleSpeaker, rightSpeaker
        )
        Sprecher.write_nrSeqs(  
            participant, blockNr,
            leftSpeaker, middleSpeaker, rightSpeaker 
        )
        Sprecher.write_nSnippets(   
            leftSpeaker, middleSpeaker, rightSpeaker
        )
        Sprecher.write_nSoundSnippets(  
            dictSoundData,
            leftSpeaker, middleSpeaker, rightSpeaker
        )
        Sprecher.write_soundData(   
            dictSoundData, 
            leftSpeaker, middleSpeaker, rightSpeaker 
        )
    
