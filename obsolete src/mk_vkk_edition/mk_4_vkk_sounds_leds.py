import freefield
import slab
from pathlib import Path
import numpy as np
import random
from typing import List
#_____________________________________________________________________________________________________
n_subblocks = int(1+30)
n_blocks = int(2 + (4*4)) # 2 training blocks (1 single speaker, 1 both speakers), 4 normal blocks for each condition
#_____________________________________________________________________________________________________
def initiate_processors():
    
    """ get rcx files"""
    path_play_buf_rcx = Path ("C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\amplitudeModulation_programs\\mk_vkk_edition\\standard_setup_long.rcx")
    path_button_rcx = Path ("C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\amplitudeModulation_programs\\mk_vkk_edition\\button.rcx")

    proc_list = [['RP2', 'RP2', path_button_rcx],
                 ['RX81', 'RX8', path_play_buf_rcx],
                 ['RX82', 'RX8', path_play_buf_rcx]]
    #___________________________
    
    """ initalise processors """
    freefield.initialize('dome', device=proc_list)

#_____________________________________________________________________________________________________

def generate_Sounds():
    
    """ create 1 sec snippets of amplitude modulated pinknoise
        in sum 6 types of snippets:
            base (unshifted) for 3 different fAMs (left, middle, right)
            shifted (base + shift resp.) """
    samplerate = int(48828)
    level = int(80) # Lautstaerke
    duration = float(1.0) # 1 sec muss so wegen shift, insg. pro Subblock 4 sec
    #________________________

    """ frequencies of amplitude modulation """
    fAM_base_Left = int(7) # [Hz]
    fAM_base_Middle = int(13) # integer !
    fAM_base_Right = int(17)
    shift = int(4)
    #________________________

    """ Shift is added and
    the same for all speakers"""
    fAM_shifted_Left = int( fAM_base_Left + shift )
    fAM_shifted_Middle = int( fAM_base_Middle + shift )
    fAM_shifted_Right = int( fAM_base_Right + shift )
    #_________________________________________
    """ create pinknoise snippets with duration of 1 second """
    pinknoise = slab.Sound.pinknoise(
        duration = duration, samplerate = samplerate, level = level
    )
    """ apply amplitude modulation """
    baseLeft = pinknoise.am (frequency = fAM_base_Left)
    baseMiddle = pinknoise.am (frequency = fAM_base_Middle)
    baseRight = pinknoise.am (frequency = fAM_base_Right)

    shiftedLeft = pinknoise.am (frequency = fAM_shifted_Left)
    shiftedMiddle = pinknoise.am (frequency = fAM_shifted_Middle)
    shiftedRight = pinknoise.am (frequency = fAM_shifted_Right)
    # _________________________________________
    return baseLeft, baseMiddle, baseRight, shiftedLeft, shiftedMiddle, shiftedRight
#_____________________________________________________________________________________________________ 

def generate_sequences(n_subblocks): # works as desired
    """ generates array of '_' and 'S' Strings to define whether shift occurs or not
        this is needed in order to define which sound snippet must be used
        (base or shifted sound)"""
    poss_shift_occurence = ['left', 'middle', 'right']
    shift_occurence = ['no'] # 0. subblock no shift
    for i in range (0,n_subblocks-1, 1):
        shift_occurence = shift_occurence + [random.choice (poss_shift_occurence)]

    sequenceLeft = []
    sequenceMiddle = []
    sequenceRight = []

    for i in range (0, ((n_subblocks-1)+1), 1): # length(=n_entries) shift_occurence = n_subblocks-1 !
        if shift_occurence[i] == 'no':
            sequenceLeft = sequenceLeft +  ['_'] + ['_'] + ['_'] + ['_']
            sequenceMiddle = sequenceMiddle + ['_'] + ['_'] + ['_'] + ['_']
            sequenceRight = sequenceRight + ['_'] + ['_'] + ['_'] + ['_']

        elif shift_occurence[i] == 'left':
            sequenceLeft = sequenceLeft +  ['S'] + ['_'] + ['_'] + ['_']
            sequenceMiddle = sequenceMiddle + ['_'] + ['_'] + ['_'] + ['_']
            sequenceRight = sequenceRight + ['_'] + ['_'] + ['_'] + ['_']

        elif shift_occurence[i] == 'middle':
            sequenceLeft = sequenceLeft +  ['_'] + ['_'] + ['_'] + ['_']
            sequenceMiddle = sequenceMiddle + ['S'] + ['_'] + ['_'] + ['_']
            sequenceRight = sequenceRight + ['_'] + ['_'] + ['_'] + ['_']

        elif shift_occurence[i] == 'right':
            sequenceLeft = sequenceLeft +  ['_'] + ['_'] + ['_'] + ['_']
            sequenceMiddle = sequenceMiddle + ['_'] + ['_'] + ['_'] + ['_']
            sequenceRight = sequenceRight + ['S'] + ['_'] + ['_'] + ['_']

            print(len(sequenceLeft))     # n_entries = 4 * n_subblocks
            print(len(sequenceMiddle))
            print(len(sequenceRight))
            print(shift_occurence)
            print(sequenceLeft)
            print(sequenceMiddle)
            print(sequenceRight)

    #_________________________________________________
    return sequenceLeft, sequenceMiddle, sequenceRight
#_____________________________________________________________________________________________________ 

def get_sequence_labels_list(sequence_X, nums=[]):
    """ makes number arrays out of array with shift occurence
    e.g.    sequence_X: ['_', 'S', 'S', ...] 
            nums: [1,2]
            -> label_nums_list: [1, 2, 2] """
    # sequence_X = sequence_A XOR sequence_B XOR sequence_C
    # nums = [1,2] XOR [3,4] XOR [5,6]
    label_nums_list = []
    for label in sequence_X:
        if label == "_": # label = entry in sequence_X
         nr = nums[0]
         label_nums_list.append(nr)
        elif label == "S":
            nr = nums[1]
            label_nums_list.append(nr)
        else:
            print("'''''\n CAVE: Generation of label_nums_list failed. \n'''''")
    return label_nums_list
#_____________________________________________________________________________________________________ 

def gen_sequence_indices(sequenceLeft, sequenceMiddle, sequenceRight):
    """ apply function get_sequence_labels_list(sequence_X, nums=[])
    for each speaker

    # even numbers: base (unshifted) resp.
    # odd numbers : shifted resp.

    different speakers acquire different numbers
    """
    
    label_nums_list_Left = get_sequence_labels_list(sequenceLeft, nums=[1, 2])
    label_nums_list_Middle = get_sequence_labels_list(sequenceMiddle, nums=[3, 4])
    label_nums_list_Right = get_sequence_labels_list(sequenceRight, nums=[5, 6])

    numSeqLeft = np.array(label_nums_list_Left).astype('int32')
    numSeqLeft = np.append(0, numSeqLeft)

    numSeqMiddle = np.array(label_nums_list_Middle).astype('int32')
    numSeqMiddle = np.append(0, numSeqMiddle)

    numSeqRight = np.array(label_nums_list_Right).astype('int32')
    numSeqRight = np.append(0, numSeqRight)

    return numSeqLeft, numSeqMiddle, numSeqRight
#_____________________________________________________________________________________________________   

def pick_write_and_apply_filters(baseLeft, baseMiddle, baseRight, shiftedLeft, shiftedMiddle, shiftedRight):
    
    """ adress speakers """
    speaker_coordinates_LMR = [(-35,0), (0,0), (35,0)]

    [speakerLeft] = freefield.pick_speakers((speaker_coordinates_LMR[0]))
    [speakerMiddle] = freefield.pick_speakers((speaker_coordinates_LMR[1]))
    [speakerRight] = freefield.pick_speakers((speaker_coordinates_LMR[2]))
    #_____________________________________________________________________ 

    """ equals level for all sounds """
    filterLeft = speakerLeft.filter
    filterLeft.apply(baseLeft)
    filterLeft.apply(shiftedLeft)

    filterMiddle = speakerMiddle.filter
    filterMiddle.apply(baseMiddle)
    filterMiddle.apply(shiftedMiddle)

    filterRight = speakerRight.filter
    filterRight.apply(baseRight)
    filterRight.apply(shiftedRight)
    #_____________________________________________________________________
    
    """ write channel identity """
    freefield.write('channelLeft', speakerLeft.analog_channel, speakerLeft.analog_proc)
    #processors = ['RX81', 'RX82']
    #processors.remove(speaker_A.analog_proc)
    #freefield.write('channel_A', 0, processors)

    freefield.write('channelMiddle', speakerMiddle.analog_channel, speakerMiddle.analog_proc)
    #processors = ['RX81', 'RX82']
    #processors.remove(speaker_B.analog_proc)
    #freefield.write('channel_B', 0, processors)

    freefield.write('channelRight', speakerRight.analog_channel, speakerRight.analog_proc)
    #processors = ['RX81', 'RX82']
    #processors.remove(speaker_C.analog_proc)
    #freefield.write('channel_C', 0, processors)

    #_____________________________________________________________________
    
    """ write sounds (1 sec snippets)"""
    freefield.write('baseLeft_data', baseLeft.data, ['RX81', 'RX82'])
    freefield.write('baseLeft_n_samples', baseLeft.n_samples, ['RX81', 'RX82'])
    
    freefield.write('shiftedLeft_data', shiftedLeft.data, ['RX81', 'RX82'])
    freefield.write('shiftedLeft_n_samples', shiftedLeft.n_samples, ['RX81', 'RX82'])
    

    freefield.write('baseMiddle_data', baseMiddle.data, ['RX81', 'RX82'])
    freefield.write('baseMiddle_n_samples', baseMiddle.n_samples, ['RX81', 'RX82'])

    freefield.write('shiftedMiddle_data', shiftedMiddle.data, ['RX81', 'RX82'])
    freefield.write('shiftedMiddle_n_samples', shiftedMiddle.n_samples, ['RX81', 'RX82'])
    

    freefield.write('baseRight_data', baseRight.data, ['RX81', 'RX82'])
    freefield.write('baseRight_n_samples', baseRight.n_samples, ['RX81', 'RX82'])

    freefield.write('shiftedRight_data', shiftedRight.data, ['RX81', 'RX82'])
    freefield.write('shiftedRight_n_samples', shiftedRight.n_samples, ['RX81', 'RX82'])
    #_____________________________________________________________________
    
    sequenceLeft, sequenceMiddle, sequenceRight = generate_sequences()
    freefield.write('n_trials_Left', len(sequenceLeft), ['RX81', 'RX82'])
    freefield.write('n_trials_Middle', len(sequenceMiddle), ['RX81', 'RX82'])
    freefield.write('n_trials_Right', len(sequenceRight), ['RX81', 'RX82'])
    #_____________________________________________________________________
    
    """ write shift occuence 
    i.e. kind of sound snippet (shifted/unshifted)
    (formated as numbers)"""
    numSeqLeft, numSeqMiddle, numSeqRight = gen_sequence_indices(sequenceLeft, sequenceMiddle, sequenceRight)
    freefield.write('numSeqLeft', numSeqLeft, ['RX81', 'RX82'])
    freefield.write('numSeqMiddle', numSeqMiddle, ['RX81', 'RX82'])
    freefield.write('numSeqRight', numSeqRight, ['RX81', 'RX82'])
#______________________________________________________________________________________________________
def generate_target_list(n_subblocks):
    target_possibilities = ['left', 'middle', 'right', 'both']
    start_target = random.choice
    target_list = []
    #export
#________________________________________________________________________________________________________________
def turn_target_led_on(target):
    led_coordinates = [(0, 25), (0, 0), (0, -25)]

    [led_21] = freefield.pick_speakers((led_coordinates[0]))  # bit2 top (speaker21) ##rcx digital_channel: 4
    [led_23] = freefield.pick_speakers((led_coordinates[1]))  # bit3 centre (speaker23) ##rcx digital_channel: 8
    [led_25] = freefield.pick_speakers((led_coordinates[2]))  # bit4 centre (speaker25) ## rcx digital_channel: 16

    if target == "left":
        freefield.write('bitmaskLeft', led_21.digital_channel, led_21.digital_proc)
    elif target == "middle":
        freefield.write('bitmaskMiddle', led_23.digital_channel, led_23.digital_proc)
    elif target == "right":
        freefield.write('bitmaskRight', led_25.digital_channel, led_25.digital_proc)
    elif target == "both":
        freefield.write('bitmaskLeft', led_21.digital_channel, led_21.digital_proc)
        freefield.write('bitmaskRight', led_25.digital_channel, led_25.digital_proc)
    else:
        print("'''''\n CAVE: Invalid target for led. \n'''''")
#___________________________________________________________________________________________________________
def turn_all_leds_off():
    led_coordinates = [(0, 25), (0, 0), (0, -25)]

    [led_21] = freefield.pick_speakers((led_coordinates[0]))  # bit2 top (speaker21) ##rcx digital_channel: 4
    [led_23] = freefield.pick_speakers((led_coordinates[1]))  # bit3 centre (speaker23) ##rcx digital_channel: 8
    [led_25] = freefield.pick_speakers((led_coordinates[2]))  # bit4 centre (speaker25) ## rcx digital_channel: 16

    freefield.write('bitmaskLeft', 0, led_21.digital_proc)
    freefield.write('bitmaskMiddle', 0, led_23.digital_proc)
    freefield.write('bitmaskRight', 0, led_25.digital_proc)
#___________________________________________________________________________________________

#_____________________________________________________________________________________________________
if __name__ == "__main__":

    freefield.play(kind='zBusA')