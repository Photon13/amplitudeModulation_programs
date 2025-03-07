import freefield
import slab
from pathlib import Path
import numpy as np
import random
#_______________________________________________________________________________________________________________________________________________________
path_play_buf_rcx = Path(
    "C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\5_Bachelorarbeit\\5_Version_data_programs_etc\\Programs\\rcx\\standard_setup_long.rcx"
)
path_button_rcx = Path(
    "C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\Testing Programs\\rcx\\button.rcx"
)
proc_list = [['RP2', 'RP2', path_button_rcx],
             ['RX81', 'RX8', path_play_buf_rcx],
             ['RX82', 'RX8', path_play_buf_rcx]]

freefield.initialize('dome', device=proc_list)
#_______________________________________________________________________________________________________________________________________________________
def generate_pinknoise_segments():

    samplerate = int(48828)
    level = int(80)
    duration = float(1.0)

    fAM_base_A = int(7)
    fAM_base_B = int(13)
    fAM_base_C = int(17)
    shift = int(4)
    #________________________
    fAM_shifted_A = int( fAM_base_A + shift )
    fAM_shifted_B = int( fAM_base_B + shift )
    fAM_shifted_C = int( fAM_base_C + shift )
    #_________________________________________
    pinknoise = slab.Sound.pinknoise(
        duration = duration, samplerate = samplerate, level = level
    )
    base_A = pinknoise.am (frequency = fAM_base_A)
    base_B = pinknoise.am (frequency = fAM_base_B)
    base_C = pinknoise.am (frequency = fAM_base_C)

    shifted_A = pinknoise.am (frequency = fAM_shifted_A)
    shifted_B = pinknoise.am (frequency = fAM_shifted_B)
    shifted_C = pinknoise.am (frequency = fAM_shifted_C)

    return base_A, base_B, base_C, shifted_A, shifted_B, shifted_C

base_A, base_B, base_C, shifted_A, shifted_B, shifted_C = generate_pinknoise_segments()
#_______________________________________________________________________________________________________________________________________________________
def assign_speakers():

    speaker_coordinates_LMR = [(-35,0), (0,0), (35,0)]

    [speaker_left] = freefield.pick_speakers((speaker_coordinates_LMR[0]))
    [speaker_middle] = freefield.pick_speakers((speaker_coordinates_LMR[1]))
    [speaker_right] = freefield.pick_speakers((speaker_coordinates_LMR[2]))
    #______________________________________________________________________
    poss_speaker_position = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    speaker_position = random.choice(poss_speaker_position)
    print (speaker_position) # EXPORT !
    #_________________________________________________
    if speaker_position == "ABC":
        [speaker_A] = [speaker_left]
        [speaker_B] = [speaker_middle]
        [speaker_C] = [speaker_right]
    elif speaker_position == "ACB":
        [speaker_A] = [speaker_left]
        [speaker_C] = [speaker_middle]
        [speaker_B] = [speaker_right]
    elif speaker_position == "BAC":
        [speaker_B] = [speaker_left]
        [speaker_A] = [speaker_middle]
        [speaker_C] = [speaker_right]
    elif speaker_position == "BCA":
        [speaker_B] = [speaker_left]
        [speaker_C] = [speaker_middle]
        [speaker_A] = [speaker_right]
    elif speaker_position == "CAB":
        [speaker_C] = [speaker_left]
        [speaker_A] = [speaker_middle]
        [speaker_B] = [speaker_right]
    elif speaker_position == "CBA":
        [speaker_C] = [speaker_left]
        [speaker_B] = [speaker_middle]
        [speaker_A] = [speaker_right]
    else:
        print("'''''\n CAVE! Speakers couldn't be assigned to positions. \n'''''")

    return speaker_A, speaker_B, speaker_C

speaker_A, speaker_B, speaker_C = assign_speakers()
#_______________________________________________________________________________________________________________________________________________________
def apply_filters():

    filter_A = speaker_A.filter
    filter_A.apply(base_A)
    filter_A.apply(shifted_A)

    filter_B = speaker_B.filter
    filter_B.apply(base_B)
    filter_B.apply(shifted_B)

    filter_C = speaker_C.filter
    filter_C.apply(base_C)
    filter_C.apply(shifted_C)

apply_filters()
#_______________________________________________________________________________________________________________________________________________________
def write_channels():

    freefield.write('channel_A', speaker_A.analog_channel, speaker_A.analog_proc)
    #processors = ['RX81', 'RX82']
    #processors.remove(speaker_A.analog_proc)
    #freefield.write('channel_A', 0, processors)

    freefield.write('channel_B', speaker_B.analog_channel, speaker_B.analog_proc)
    #processors = ['RX81', 'RX82']
    #processors.remove(speaker_B.analog_proc)
    #freefield.write('channel_B', 0, processors)

    freefield.write('channel_C', speaker_C.analog_channel, speaker_C.analog_proc)
    #processors = ['RX81', 'RX82']
    #processors.remove(speaker_C.analog_proc)
    #freefield.write('channel_C', 0, processors)

write_channels()
#_______________________________________________________________________________________________________________________________________________________
def generate_sequences():
    # n_entries in shift_occurence = n_blocks
    shift_occurence = ['A', 'B', 'B', 'C'] # GET FROM EXCEL
    sequence_A = ['_', '_', '_', '_'] # subblock0 : no shift
    sequence_B = ['_', '_', '_', '_']
    sequence_C = ['_', '_', '_', '_']

    subblock_list = ['N'] # subblock0 : no shift

    i=0
    while (i<len(shift_occurence)):
        ###
        if shift_occurence[i] == 'A':

            subblock_list.append('A')

            sequence_A.append ('S')
            sequence_A.append ('_')
            sequence_A.append ('_')
            sequence_A.append ('_')

            sequence_B.append ('_')
            sequence_B.append ('_')
            sequence_B.append ('_')
            sequence_B.append ('_')

            sequence_C.append ('_')
            sequence_C.append ('_')
            sequence_C.append ('_')
            sequence_C.append ('_')
        ###
        elif shift_occurence[i] == 'B':

            subblock_list.append('B')

            sequence_A.append ('_')
            sequence_A.append ('S')
            sequence_A.append ('_')
            sequence_A.append ('_')
            sequence_A.append ('_')

            sequence_B.append ('S')
            sequence_B.append ('_')
            sequence_B.append ('_')
            sequence_B.append ('_')

            sequence_C.append ('_')
            sequence_C.append ('_')
            sequence_C.append ('_')
            sequence_C.append ('_')

        ###
        elif shift_occurence[i] == 'C':

            subblock_list.append('C')

            sequence_A.append ('_')
            sequence_A.append ('_')
            sequence_A.append ('_')
            sequence_A.append ('_')

            sequence_B.append ('_')
            sequence_B.append ('_')
            sequence_B.append ('_')
            sequence_B.append ('_')

            sequence_C.append ('S')
            sequence_C.append ('_')
            sequence_C.append ('_')
            sequence_C.append ('_')
        ###    
        else:
            print("'''''\n CAVE: Ungültiger Entry in Liste shift_occurence. \n'''''")
        ###
        i = i+1
    return sequence_A, sequence_B, sequence_C
sequence_A, sequence_B, sequence_C = generate_sequences() 
#_______________________________________________________________________________________________________________________________________________________
def get_sequence_labels_list(sequence_X, nums=[]):
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

def gen_sequence_indices(sequence_A, sequence_B, sequence_C):
    # even numbers: base (unshifted) resp.
    # odd numbers : shifted resp.

    label_nums_list_A = get_sequence_labels_list(sequence_A, nums=[1, 2])
    label_nums_list_B = get_sequence_labels_list(sequence_B, nums=[3, 4])
    label_nums_list_C = get_sequence_labels_list(sequence_C, nums=[5, 6])

    sequence_indices_A = np.array(label_nums_list_A).astype('int32')
    sequence_indices_A = np.append(0,sequence_indices_A)

    sequence_indices_B = np.array(label_nums_list_B).astype('int32')
    sequence_indices_B = np.append(0,sequence_indices_B)

    sequence_indices_C = np.array(label_nums_list_C).astype('int32')
    sequence_indices_C = np.append(0,sequence_indices_C)

    return sequence_indices_A, sequence_indices_B, sequence_indices_C

sequence_indices_A, sequence_indices_B, sequence_indices_C = gen_sequence_indices(sequence_A, sequence_B, sequence_C)
#_______________________________________________________________________________________________________________________________________________________
def write_data_samples_trials_sequence():

    freefield.write('base_A_data', base_A.data, ['RX81', 'RX82'])
    freefield.write('base_A_n_samples', base_A.n_samples, ['RX81', 'RX82'])

    freefield.write('shifted_A_data', shifted_A.data, ['RX81', 'RX82'])
    freefield.write('shifted_A_n_samples', shifted_A.n_samples, ['RX81', 'RX82'])

    freefield.write('n_trials_A', len(sequence_A), ['RX81', 'RX82'])
    freefield.write('seq_num_A', sequence_indices_A, ['RX81', 'RX82']) 
### seq contaning whether shift or not i.e. which sound (base XOR shifted)
###
    freefield.write('base_B_data', base_B.data, ['RX81', 'RX82'])
    freefield.write('base_B_n_samples', base_B.n_samples, ['RX81', 'RX82'])

    freefield.write('shifted_B_data', shifted_B.data, ['RX81', 'RX82'])
    freefield.write('shifted_B_n_samples', shifted_B.n_samples, ['RX81', 'RX82'])

    freefield.write('n_trials_B', len(sequence_C), ['RX81', 'RX82'])
    freefield.write('seq_num_B', sequence_indices_C, ['RX81', 'RX82'])
###
###
    freefield.write('base_C_data', base_C.data, ['RX81', 'RX82'])
    freefield.write('base_C_n_samples', base_C.n_samples, ['RX81', 'RX82'])

    freefield.write('shifted_C_data', shifted_C.data, ['RX81', 'RX82'])
    freefield.write('shifted_C_n_samples', shifted_C.n_samples, ['RX81', 'RX82'])

    freefield.write('n_trials_C', len(sequence_C), ['RX81', 'RX82'])
    freefield.write('seq_num_C', sequence_indices_C, ['RX81', 'RX82'])

write_data_samples_trials_sequence()
#_______________________________________________________________________________________________________________________________________________________
def assign_leds():
    #print(freefield.all_leds())
    led_coordinates = [(0,25), (0,0), (0,-25)] # (azimuth, elevation)

    [ledLeft] = freefield.pick_speakers ((led_coordinates [0])) # this one is in the middle

    [ledMiddle] = freefield.pick_speakers ((led_coordinates [1])) # this one is on top for some reason

    [ledRight] = freefield.pick_speakers ((led_coordinates [2])) # last one on bottom
    
    return ledLeft, ledMiddle, ledRight 

ledLeft, ledMiddle, ledRight = assign_leds()
#_______________________________________________________________________________________________________________________________________________________

def find_out_target(block_index): 
    """ CHANGE TO GET IT FROM EXCEL!!!"""
    #read target_sequence ('left', 'both', ...)
    target_sequence = ['left'] 
    
    target = (target_sequence[block_index])
    return target

block_index=0 #only for test now
target = find_out_target(block_index) 
print(target)
#_______________________________________________________________________________________________________________________________________________________
def turn_target_led_on (target, ledLeft, ledMiddle, ledRight):
    if target == "left":
        freefield.write('bitmask', ledLeft.digital_channel, ledLeft.digital_proc) 
    elif target == 'middle':
        freefield.write('bitmask', ledMiddle.digital_channel, ledMiddle.digital_proc) 
    elif target == 'right':
        freefield.write('bitmask', ledRight.digital_channel, ledRight.digital_proc) 
    elif target == 'both':
        freefield.write('bitmask', ledLeft.digital_channel, ledLeft.digital_proc)
        freefield.write('bitmask', ledRight.digital_channel, ledRight.digital_proc)


def turn_target_led_off(ledLeft, ledMiddle, ledRight):

    freefield.write("bitmask", 0, ledLeft.digital_proc)
    freefield.write("bitmask", 0, ledMiddle.digital_proc)
    freefield.write("bitmask", 0, ledRight.digital_proc)
#_______________________________________________________________________________________________________________________________________________________


n_blocks = 3

def run_experiment(n_blocks):
    
    while True:
        participant_nr = input ("\n >>> Participant number?: ")
        participant_nr = int(participant_nr)
        bestaetigung = input (f"\n Participant number is {participant_nr}. \n >>> Bestätigen? yes/no: ")
        if bestaetigung.lowerCase() == "yes":
            break

    block_index = int(0) # first training block (for 1 target)
    while True:
        i = input ("\n Start 0.block (training)? >>> yes:")
        if i.lowerCase() == "yes":
            break
    run_block()

    block_index = int(1) # second training block (for 'both' = target)
    while True:
        i = input ("\n Start 1.block (training)? >>> yes:")
        if i.lowerCase() == "yes":
            break
    run_block()
        
    block_index = block_index + 1 
    for block_index in range (1, n_blocks, 1):

        while True:
            i = input ("\n Continue with next block? >>> yes/ABBRUCH: ")
            if i.lowerCase() == "abbruch":
                print("Bist du sicher, dass du das Experiment abbrechen möchtest? \n Bisher gewonnene Daten werden gespeichert und exportiert.")
                bestaetigung = input ("Abbruch Bestätigen >>> JA/NEIN: ")
                if bestaetigung.lowerCase() == "ja":
                    #exportiere Daten
                    break
                    #beende programm
                #else -> false -> repeat loop



            elif i.lowerCase() == "yes":
                run_block()
                break
            #else
                #repeat loop
        #block_index = block_index +1 (automatisch for-Schleife)

def run_block():

    turn_target_led_on (target, ledLeft, ledMiddle, ledRight)
    freefield.play(kind='zBusA') #only triggers sounds?

    """WAIT UNTIL DONE"""
    turn_target_led_off(target, ledLeft, ledMiddle, ledRight)



"""recreate led sheet for leds"""

"""RCX 1->A, 2->B und 3->C ändern bei tags """ #erledigt

"""CAVE: LED links und rechts müssen 
untersch Prozessoren benutzen wegen both condition !!!"""

"""concatenate all functions for 1 block (block_index++ etc)"""