import freefield

from Globals import Globals
from SoundMxxk import SoundMxxk

class SpeakerMethods:

    def write_toSpeakers(participant, block_nr):

        [leftSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[0]) # freefield.pick_speakers((speakersCoordinates[1]))
        [middleSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[1])
        [rightSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[2])

        freefield.write("channelLeft", leftSpeaker.analog_channel, leftSpeaker.analog_proc)
        freefield.write("channelMiddle", middleSpeaker.analog_channel, middleSpeaker.analog_proc)
        freefield.write("channelRight", rightSpeaker.analog_channel, rightSpeaker.analog_proc)
    
        # send sequence of number onto rcx:
        # ( for left: 1 (= no shift) or 2 (= shift), resp.;
        #   for left: 3 (= no shift) or 4 (= shift), resp.;
        #   for left: 5 (= no shift) or 6 (= shift), resp. )
        # nrSeqs are attributes of Block instances
        # Participant aggregates Block instances
        # Block instances are: block_0, block_1, ...
        # the current participant is just called participant (at least during the experiment)
        freefield.write("nrSeqLeft", participant.blockDict[f"block_{block_nr}"].nrSeqLeft, leftSpeaker.analog_proc)
        freefield.write("nrSeqMiddle", participant.blockDict[f"block_{block_nr}"].nrSeqMiddle, middleSpeaker.analog_proc)
        freefield.write("nrSeqRight", participant.blockDict[f"block_{block_nr}"].nrSeqRight, rightSpeaker.analog_proc)

        freefield.write("n_snippetsLeft", (Globals.N_SUBBLOCKS *4), leftSpeaker.analog_proc)
        freefield.write("n_snippetsMiddle", (Globals.N_SUBBLOCKS *4), middleSpeaker.analog_proc)
        freefield.write("n_snippetsRight", (Globals.N_SUBBLOCKS *4), rightSpeaker.analog_proc)

        # send number of samples onto rcx
        SoundMxxk.set_soundSnippets(participant)
        freefield.write("baseLeft_n_samples", SoundMxxk.dictSoundData["soundLeft_base"].n_samples, leftSpeaker.analog_proc)
        freefield.write("baseMiddle_n_samples", SoundMxxk.dictSoundData["soundMiddle_base"].n_samples, middleSpeaker.analog_proc)
        freefield.write("baseRight_n_samples", SoundMxxk.dictSoundData["soundRight_base"].n_samples, rightSpeaker.analog_proc)

        freefield.write("shiftedLeft_n_samples", SoundMxxk.dictSoundData["soundLeft_shifted"].n_samples, leftSpeaker.analog_proc)
        freefield.write("shiftedMiddle_n_samples", SoundMxxk.dictSoundData["soundMiddle_shifted"].n_samples, middleSpeaker.analog_proc)
        freefield.write("shiftedRight_n_samples", SoundMxxk.dictSoundData["soundRight_shifted"].n_samples, rightSpeaker.analog_proc)

        # send sound data (data per snippet type) onto rcx
        freefield.write("baseLeft_data", SoundMxxk.dictSoundData["soundLeft_base"].data, leftSpeaker.analog_proc)
        freefield.write("baseMiddle_data", SoundMxxk.dictSoundData["soundMiddle_base"].data, middleSpeaker.analog_proc)
        freefield.write("baseRight_data", SoundMxxk.dictSoundData["soundRight_base"].data, rightSpeaker.analog_proc)

        freefield.write("shiftedLeft_data", SoundMxxk.dictSoundData["soundLeft_shifted"].data, leftSpeaker.analog_proc)
        freefield.write("shiftedMiddle_data", SoundMxxk.dictSoundData["soundMiddle_shifted"].data, middleSpeaker.analog_proc)
        freefield.write("shiftedRight_data", SoundMxxk.dictSoundData["soundRight_shifted"].data, rightSpeaker.analog_proc)
