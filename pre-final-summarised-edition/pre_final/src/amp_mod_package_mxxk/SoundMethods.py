import slab

import SpeakerMethods


class SoundMethods:

    # only at start experiment
    @staticmethod
    def generate_soundSnippets(): # seems to work (?)
        famLeft_base, famLeft_shifted, famMiddle_base, famMiddle_shifted, famRight_base, famRight_shifted = SpeakerMethods.SpeakerMethods.randomise_speakers()

        samplerate = 48828
        level = 80
        duration = 1.0 # float!

        pinknoise = slab.Sound.pinknoise( duration= duration, samplerate= samplerate, level= level)

        soundLeft_base = pinknoise.am( frequency= famLeft_base)
        soundLeft_shifted = pinknoise.am( frequency= famLeft_shifted)

        soundMiddle_base = pinknoise.am( frequency= famMiddle_base)
        soundMiddle_shifted = pinknoise.am( frequency= famMiddle_shifted)

        soundRight_base = pinknoise.am( frequency= famRight_base)
        soundRight_shifted = pinknoise.am( frequency= famRight_shifted)

        soundList = [soundLeft_base, soundLeft_shifted, soundMiddle_base, soundMiddle_shifted, soundRight_base, soundRight_shifted]

        return soundList