import slab

from Globals import Globals

class SoundMxxk:

    # only at start experiment
    @classmethod
    def set_soundSnippets(cls, participant): # seems to work (?)
        famLeft_base = participant.fam_LMR_base_list[0]
        famMiddle_base = participant.fam_LMR_base_list[1]
        famRight_base = participant.fam_LMR_base_list[2]

        famLeft_shifted = participant.fam_LMR_shifted_list[0]
        famMiddle_shifted = participant.fam_LMR_shifted_list[1]
        famRight_shifted = participant.fam_LMR_shifted_list[2]

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

        #soundList = [soundLeft_base, soundLeft_shifted, soundMiddle_base, soundMiddle_shifted, soundRight_base, soundRight_shifted]

        # dictionary[key, value]
        Dict = {"soundLeft_base": soundLeft_base,
                "soundLeft_shifted": soundLeft_shifted,
                "soundMiddle_base": soundMiddle_base,
                "soundMiddle_shifted": soundMiddle_shifted,
                "soundRight_base": soundRight_base,
                "soundRight_shifted": soundRight_shifted}

        cls.dictSoundData = Dict

@staticmethod # does not work? ## but probably abundant to use getter, anyway
def get_soundSnippets(cls):
        print(cls.dictSoundData)
        return cls.dictSoundData