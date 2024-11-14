import freefield
import slab
from pathlib import Path
import numpy as np
import random
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
    
    """ sound snippets will be 1 second resp. """
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

def generate_sequences():
    
    n_subblocks = int(2+30)

    sequenceLeft = ['_', '_', '_', '_'] # subblock0 : no shift
    sequenceRight = ['_', '_', '_', '_']
    sequenceMiddle = ['_', '_', '_', '_']

    shift_occurence = random.choice('A', 'B', 'C', 'D')

    for i in range (0, n_subblocks+1, 1):
        ###
        if shift_occurence[i] == 'A':

            sequenceLeft.append ('S')
            sequenceLeft.append ('_')
            sequenceLeft.append ('_')
            sequenceLeft.append ('_')

            sequenceMiddle.append ('_')
            sequenceMiddle.append ('_')
            sequenceMiddle.append ('_')
            sequenceMiddle.append ('_')

            sequenceRight.append ('_')
            sequenceRight.append ('_')
            sequenceRight.append ('_')
            sequenceRight.append ('_')
        ###
        elif shift_occurence[i] == 'B':

            sequenceLeft.append ('_')
            sequenceLeft.append ('S')
            sequenceLeft.append ('_')
            sequenceLeft.append ('_')

            sequenceMiddle.append ('S')
            sequenceMiddle.append ('_')
            sequenceMiddle.append ('_')
            sequenceMiddle.append ('_')

            sequenceRight.append ('_')
            sequenceRight.append ('_')
            sequenceRight.append ('_')
            sequenceRight.append ('_')

        ###
        elif shift_occurence[i] == 'C':

            sequenceLeft.append ('_')
            sequenceLeft.append ('_')
            sequenceLeft.append ('_')
            sequenceLeft.append ('_')

            sequenceMiddle.append ('_')
            sequenceMiddle.append ('_')
            sequenceMiddle.append ('_')
            sequenceMiddle.append ('_')

            sequenceRight.append ('S')
            sequenceRight.append ('_')
            sequenceRight.append ('_')
            sequenceRight.append ('_')
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
    
    label_nums_list_A = get_sequence_labels_list(sequenceLeft, nums=[1, 2])
    label_nums_list_B = get_sequence_labels_list(sequenceMiddle, nums=[3, 4])
    label_nums_list_C = get_sequence_labels_list(sequenceRight, nums=[5, 6])

    numSeqLeft = np.array(label_nums_list_A).astype('int32')
    numSeqLeft = np.append(0, numSeqLeft)

    numSeqMiddle = np.array(label_nums_list_B).astype('int32')
    numSeqMiddle = np.append(0, numSeqMiddle)

    numSeqRight = np.array(label_nums_list_C).astype('int32')
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
    filter_A = speakerLeft.filter
    filter_A.apply(baseLeft)
    filter_A.apply(shiftedLeft)

    filter_B = speakerMiddle.filter
    filter_B.apply(baseMiddle)
    filter_B.apply(shiftedMiddle)

    filter_C = speakerRight.filter
    filter_C.apply(baseRight)
    filter_C.apply(shiftedRight)
    #_____________________________________________________________________
    
    """ write channel identity """
    freefield.write('channel_A', speakerLeft.analog_channel, speakerLeft.analog_proc)
    #processors = ['RX81', 'RX82']
    #processors.remove(speaker_A.analog_proc)
    #freefield.write('channel_A', 0, processors)

    freefield.write('channel_B', speakerMiddle.analog_channel, speakerMiddle.analog_proc)
    #processors = ['RX81', 'RX82']
    #processors.remove(speaker_B.analog_proc)
    #freefield.write('channel_B', 0, processors)

    freefield.write('channel_C', speakerRight.analog_channel, speakerRight.analog_proc)
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

    #_____________________________________________________________________
    

    TARGET
    
    """ adress LEDs """
    led_coordinates = [(0, 25), (0, 0), (0, -25)]  # (azimuth, elevation)

    [ledLeft] = freefield.pick_speakers((led_coordinates[0]))  # this one is in the middle
    [ledMiddle] = freefield.pick_speakers((led_coordinates[1]))  # this one is on top for some reason
    [ledRight] = freefield.pick_speakers((led_coordinates[2]))  # last one on bottom


    TURN LED OFF


#_____________________________________________________________________________________________________
if __name__ == "__main__":

    freefield.play(kind='zBusA')