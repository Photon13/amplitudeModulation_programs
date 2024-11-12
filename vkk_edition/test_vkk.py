
import freefield
import slab
from pathlib import Path
import numpy as np

path_play_buf_rcx = Path("C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\5_Bachelorarbeit\\5_Version_data_programs_etc\\Programs\\rcx\\standard_setup_long.rcx")
path_button_rcx = Path("C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\Testing Programs\\rcx\\button.rcx")
proc_list = [['RP2', 'RP2', path_button_rcx],
             ['RX81', 'RX8', path_play_buf_rcx],
             ['RX82', 'RX8', path_play_buf_rcx]]
#freefield.initialize_setup(setup="dome", default="loctest_freefield") #not working?

freefield.initialize('dome', device=proc_list)

samplerate = 48828
# todo: adjust your pink noises and their modified versions as you want, based on the ones you created; these are random
pinknoise1 = slab.Sound.pinknoise(duration=1.0, samplerate=samplerate, level=80)
pinknoise2 = slab.Sound.pinknoise(duration=1.0, samplerate=samplerate, level=80)
pinknoise2 = pinknoise2.am(frequency=33)
pinknoise3 = slab.Sound.pinknoise(duration=1.0, samplerate=samplerate, level=80)
pinknoise3 = pinknoise3.am(frequency=46)

pinknoise1_data = pinknoise1.data
pinknoise1_mod = pinknoise1.am(frequency=20)
pinknoise1_mod_data = pinknoise1_mod.data

pinknoise2_data = pinknoise2.data
pinknoise2_mod = pinknoise2.am(frequency=13)
pinknoise2_mod_data = pinknoise2_mod.data

pinknoise3_data = pinknoise3.data
pinknoise3_mod = pinknoise3.am(frequency=35)
pinknoise3_mod_data = pinknoise3_mod.data


# define the three speakers you want to use per block
speakers_coordinates = [(0, 0), (35, 0), (-35, 0)]
[speaker1] = freefield.pick_speakers((speakers_coordinates[1]))
[speaker2] = freefield.pick_speakers((speakers_coordinates[2]))
[speaker3] = freefield.pick_speakers((speakers_coordinates[0]))


# todo: we apply a filter on each sound, based from which speaker (1, 2, or 3) they will be played from
filter1 = speaker1.filter
filter1.apply(pinknoise1)
filter1.apply(pinknoise1_mod)

filter2 = speaker2.filter
filter2.apply(pinknoise2)
filter2.apply(pinknoise2_mod)

filter3 = speaker3.filter
filter3.apply(pinknoise3)
filter3.apply(pinknoise3_mod)



freefield.write('channel1', speaker1.analog_channel, speaker1.analog_proc)  # works
processors = ['RX81', 'RX82']
processors.remove(speaker1.analog_proc)
freefield.write('channel2', speaker2.analog_channel, speaker2.analog_proc)  # works
processors = ['RX81', 'RX82']

freefield.write('channel3', speaker3.analog_channel, speaker3.analog_proc)  # works
processors = ['RX81', 'RX82']
processors.remove(speaker3.analog_proc)
# freefield.write('channel', 25, processors)


duration = 120
total_trials = 120
n_trials_target = int((duration * 20) / 100)
n_trials_default = int(total_trials - n_trials_target)
pink_seq = ['pink'] * n_trials_default
pink_am_seq = ['pink_am'] * n_trials_target
sequence = np.concatenate((pink_seq, pink_am_seq))

#todo: you have your own sequence of the three different streams, these are just some I created as an example.
sequence1 = sequence.tolist()
sequence2 = sequence.tolist()
sequence3 = sequence.tolist()

# create the three randomized sequence of pink noises and their AM versions, as you desire:
np.random.shuffle(sequence1)
np.random.shuffle(sequence2)
np.random.shuffle(sequence3)

def get_sequence_labels_list(sequence, nums=[]):
    label_nums_list = []
    for label in sequence:
        if label == 'pink':
            num = nums[0]
            label_nums_list.append(num)
        else:
            num = nums[1]
            label_nums_list.append(num)
    return label_nums_list

#todo: here I assigned a number to the different sounds of each stream:
# todo: stream 1: pink default = 1, pink_am = 2; stream 2: pink default = 3, pink_am = 4; stream 3: pink default = 5, pink_am = 6
label_nums_list1 = get_sequence_labels_list(sequence1, nums=[1, 2])
label_nums_list2 = get_sequence_labels_list(sequence2, nums=[3, 4])
label_nums_list3 = get_sequence_labels_list(sequence3, nums=[5, 6])

# this is needed for rcx -> converting the data into int32; don't ask why, IDK lol.
# todo: what happens here: rcx will go from one index to the next in sequence_indices
# todo: stream 1 would be for example, something like this: 1, 2, 1, 1, 1, 2, 1, [...].
# todo: in the rcx file, whenever 1 is presented, pink default is played. when 2, pink_am (target sound)
# this is done for all 3 streams here
sequence_indices1 = np.array(label_nums_list1).astype('int32')
sequence_indices1 = np.append(0, sequence_indices1)
sequence_indices2 = np.array(label_nums_list2).astype('int32')
sequence_indices2 = np.append(0, sequence_indices2)
sequence_indices3 = np.array(label_nums_list3).astype('int32')
sequence_indices3 = np.append(0, sequence_indices3)


# channel 1 data:
freefield.write('pink_data1', pinknoise1_data, ['RX81', 'RX82']) # correct
freefield.write('pink_n_samples1', pinknoise1.n_samples, ['RX81', 'RX82'])  # correct
freefield.write('pink_am_data1', pinknoise1_mod_data, ['RX81', 'RX82']) # correct
freefield.write('pink_am_n_samples1', pinknoise1_mod.n_samples, ['RX81', 'RX82'])  # correct
freefield.write('n_trials1', total_trials + 1, ['RX81', 'RX82'])  # works
freefield.write('sequence1', sequence_indices1, ['RX81', 'RX82'])  # works

#channel 2 data:
freefield.write('pink_data2', pinknoise2_data, ['RX82', 'RX82']) # correct
freefield.write('pink_n_samples2', pinknoise2.n_samples, ['RX82', 'RX82'])  # correct
freefield.write('pink_am_data2', pinknoise2_mod_data, ['RX82', 'RX82']) # correct
freefield.write('pink_am_n_samples2', pinknoise2_mod.n_samples, ['RX82', 'RX82'])  # correct
freefield.write('n_trials2', total_trials + 2, ['RX82', 'RX82'])  # works
freefield.write('sequence2', sequence_indices2, ['RX82', 'RX82'])  # works

# channel 3 data (midline)
freefield.write('pink_data3', pinknoise3_data, ['RX81', 'RX82']) # correct
freefield.write('pink_n_samples3', pinknoise3.n_samples, ['RX81', 'RX82'])  # correct
freefield.write('pink_am_data3', pinknoise3_mod_data, ['RX81', 'RX82']) # correct
freefield.write('pink_am_n_samples3', pinknoise3_mod.n_samples, ['RX81', 'RX82'])  # correct
freefield.write('n_trials3', total_trials + 3, ['RX81', 'RX82'])  # works
freefield.write('sequence3', sequence_indices3, ['RX81', 'RX82'])  # works

freefield.play(kind='zBusA')
