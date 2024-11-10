import freefield
import slab
from slab import Sound
import numpy as np
import time
import random
from pathlib import Path
import os



#____________________________________________________________________________________________________________________________________________________________________________
target = "(left=target)" # !!!


fAM_left = 17.0
fAM_middle = 13.3
fAM_right = 15.7
shift = 16.0

sec1_duration = 1.0  # seconds
sec3_duration = 3.0  # seconds
sec4_duration = sec1_duration + sec3_duration  # 4 seconds in total

conditions = ["(shift=left)", "(shift=middle)", "(shift=right)", "(shift=NO)"]
n_subblocks = 1+30

#____________________________________________________________________________________________________________________________________________________________________________

def amplitude_modulate(sound, modulation_freq):
    """Applies amplitude modulation at a given frequency."""
    t = np.linspace(0, sound.duration, int(samplerate * sound.duration), endpoint=False)
    modulator = 0.5 * (1 + np.sin(2 * np.pi * modulation_freq * t))  # Normalize between 0 and 1
    modulated_sound = sound * modulator
    return slab.Sound(modulated_sound, samplerate=samplerate)
"""
#____________________________________________________________________________________________________________________________________________________________________________
"""
def turn_target_led_on(target): # digital processors are used for LEDs, analog processors for speakers
    if target == "(left=target)":
        freefield.write(tag="bitmask", value=led_left.digital_channel, processors=led_left.digital_proc)
        freefield.write(tag="bitmask", value=0, processors=led_middle.digital_proc)
        freefield.write(tag="bitmask", value=0, processors=led_right.digital_proc)
    elif target == "(middle=target)":
        freefield.write(tag="bitmask", value=0, processors=led_left.digital_proc)
        freefield.write(tag="bitmask", value=led_middle.digital_channel, processors=led_middle.digital_proc)
        freefield.write(tag="bitmask", value=0, processors=led_right.digital_proc)
    elif target == "(right=target)":
        freefield.write(tag="bitmask", value=0, processors=led_left.digital_proc)
        freefield.write(tag="bitmask", value=0, processors=led_middle.digital_proc)
        freefield.write(tag="bitmask", value=led_right.digital_channel, processors=led_right.digital_proc)

    elif target == "(both=target)":
        freefield.write(tag="bitmask", value=led_left.digital_channel, processors=led_left.digital_proc)
        freefield.write(tag="bitmask", value=0, processors=led_middle.digital_proc)
        freefield.write(tag="bitmask", value=led_right.digital_channel, processors=led_right.digital_proc)

    else:
        print ("'''''\n CAVE: Target LED couldn't be turned on! \n'''''")

def turn_all_leds_off():
    freefield.write(tag="bitmask", value=led_left.digital_channel, processors=led_left.digital_proc)
    freefield.write(tag="bitmask", value=led_middle.digital_channel, processors=led_middle.digital_proc)
    freefield.write(tag="bitmask", value=led_right.digital_channel, processors=led_right.digital_proc)

#____________________________________________________________________________________________________________________________________________________________________________

#samplerate = slab.Signal.default_samplerate()
samplerate=slab.get_default_samplerate()
#samplerate = 41700 # correct default?

sec3_sound = slab.Sound.pinknoise(duration=sec3_duration, samplerate=samplerate)
sec1_sound = slab.Sound.pinknoise(duration=sec1_duration, samplerate=samplerate)
sec4_sound = slab.Sound.pinknoise(duration=sec4_duration, samplerate=samplerate)

#sec3_sound.play()
"""
"""
#sec3_left = amplitude_modulate(sec3_sound, fAM_left)
#sec3_middle = amplitude_modulate(sec3_sound, fAM_middle)
#sec3_right = amplitude_modulate(sec3_sound, fAM_right)

#sec1_left = amplitude_modulate(sec1_sound, (fAM_left+shift))
#sec1_middle = amplitude_modulate(sec1_sound, (fAM_middle+shift))
#sec1_right = amplitude_modulate(sec1_sound, (fAM_right+shift))

#frequency=10, depth=1, phase=0

sec3_left = sec3_sound.am(fAM_left, 1)
sec3_middle = sec3_sound.am(fAM_middle, 1)
sec3_right = sec3_sound.am(fAM_right, 1)

sec1_left = sec1_sound.am(fAM_left, 1)
sec1_middle = sec1_sound.am(fAM_middle, 1)
sec1_right = sec1_sound.am(fAM_right, 1)

#sec3_1_left = sec3_1_sound.am(fAM_left, 1)
#sec3_1_middle = sec3_1_sound.am(fAM_middle, 1)
#sec3_1_right = sec3_1_sound.am(fAM_right, 1)

sec4_left = sec4_sound.am(fAM_left, 1)
sec4_middle = sec4_sound.am(fAM_middle, 1)
sec4_right = sec4_sound.am(fAM_right, 1)


#sec1_left = amplitude_modulate(sec1_sound, (fAM_left+shift))
#sec1_middle = amplitude_modulate(sec1_sound, (fAM_middle+shift))
#sec1_right = amplitude_modulate(sec1_sound, (fAM_right+shift))

sec3_1_left = sec1_left + sec3_left # incl. shift
sec3_1_middle = sec1_middle + sec3_middle 
sec3_1_right = sec1_right + sec3_right

#sec4_left = amplitude_modulate(sec4_sound, fAM_left) # excl. shift
#sec4_middle = amplitude_modulate(sec4_sound, fAM_middle)
#sec4_right = amplitude_modulate(sec4_sound, fAM_right)

sec4_left=slab.Sound(sec4_left)
sec4_middle=slab.Sound(sec4_middle)
sec4_right=slab.Sound(sec4_right)

sec3_1_left=slab.Sound(sec3_1_left)
sec3_1_middle=slab.Sound(sec3_1_middle)
sec3_1_right=slab.Sound(sec3_1_right)

#____________________________________________________________________________________________________________________________________________________________________________
"""
initialize_setup(setup, default_mode=None, proc_list=None, zbus=True, connection="GB", camera_type=None)
>>>>> initialize_setup("dome", default_mode="loctest_freefield")
            if only default_mode given:
                PROCESSORS.initialize_default(default_mode):
                    ->defines proc_list
                    ->PROCESSORS.initialize(proc_list, True, 'GB')
"""
#____________________________________________________________________________________________________________________________________________________________________________

# sound = Sound.read("path_to_your_file.wav")
# freefield.play_sound(sound) # Sound = class from slab

# ? ? ? freefield.set_output(channel="dome")  # Use the dome configuration

#____________________________________________________________________________________________________________________________________________________________________________

if __name__ == "__main__":

    path_play_buf_rcx =  Path("C:\\projects\\Maik Kuerschner\\Biologie Bachelor\\Bachelorarbeit\\Testing Programs\\rcx\\play_buf.rcx")
    path_button_rcx = Path("C:\\projects\\Maik Kuerschner\\Biologie Bachelor\\Bachelorarbeit\\Testing Programs\\rcx\\button.rcx")
    proc_list = [['RP2', 'RP2', path_button_rcx],
                 ['RX81', 'RX8', path_play_buf_rcx],
                 ['RX82', 'RX8', path_play_buf_rcx]]
    #freefield.initialize_setup(setup="dome", default="loctest_freefield") #not working?

    freefield.initialize('dome', zbus=True, device=proc_list)

    slab.set_default_samplerate(44100)
    DIR = Path(os.getcwd())

    speakers = [8, 23, 38]

    #speaker_left = freefield.pick_speakers(8)
    #speaker_middle = freefield.pick_speakers(23)
    #speaker_right = freefield.pick_speakers(38)

    [speaker_left] = freefield.pick_speakers((-35, 0))
    [speaker_middle] = freefield.pick_speakers((0, 0))
    [speaker_right] = freefield.pick_speakers((35, 0))

    [led_left] = freefield.pick_speakers((0, 25))
    [led_middle] = freefield.pick_speakers((0, 0))
    [led_right] = freefield.pick_speakers((0, -25))

    #[speaker_left] = freefield.pick_speakers([-35, 0])
    #[speaker_middle] = freefield.pick_speakers([0, 0])
    #[speaker_right] = freefield.pick_speakers([35, 0])

    #speaker_left = int(8)
    #speaker_middle = int(23)
    #speaker_right = int(38)

    #set_speaker(speaker) ??





    #led_left = freefield.pick_speakers(speaker_left) # ???
    #led_middle = freefield.pick_speakers(speaker_middle)
    #led_right = freefield.pick_speakers(speaker_right)

    #____________________________________________________________________________________________________________________________________________________________________________
    
    print("Starting loop.")
    for i in range (n_subblocks):
        index_subblock = i
        condition = random.choice(conditions) # Change later to excel
        #set_signal_and_speaker(signal, speaker, equalize=True, data_tag='data', chan_tag='chan',n_samples_tag='playbuflen')
        if condition == "(shift=NO)":
            freefield.set_signal_and_speaker(signal=sec4_left, speaker=speaker_left)
            freefield.set_signal_and_speaker(signal=sec4_middle, speaker=speaker_middle)
            freefield.set_signal_and_speaker(signal=sec4_right, speaker=speaker_right)
        
        elif condition == "(shift=left)":
            freefield.set_signal_and_speaker(signal=sec3_1_left, speaker = speaker_left)
            freefield.set_signal_and_speaker(signal=sec4_middle, speaker = speaker_middle)
            freefield.set_signal_and_speaker(signal=sec4_right, speaker = speaker_right)

        elif condition == "(shift=middle)":
            freefield.set_signal_and_speaker(signal=sec4_left, speaker = speaker_left)
            freefield.set_signal_and_speaker(signal=sec3_1_middle, speaker = speaker_middle)
            freefield.set_signal_and_speaker(signal=sec4_right, speaker = speaker_right)

        elif condition == "(shift=right)":
            freefield.set_signal_and_speaker(signal=sec4_left, speaker = speaker_left)
            freefield.set_signal_and_speaker(signal=sec4_middle, speaker = speaker_middle)
            freefield.set_signal_and_speaker(signal=sec3_1_right, speaker = speaker_right)
        else:
            print ("'''''\n CAVE: Invalid condition given! \n'''''")

        turn_target_led_on(target)
        #freefield.play(kind='zBusA')
        #freefield.wait_to_finish_playing()
        turn_all_leds_off()
