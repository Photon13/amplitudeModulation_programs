
import freefield
import slab
from pathlib import Path
import numpy as np

path_play_buf_rcx = Path("C:\\projects\\Maik Kuerschner\\Biologie Bachelor\\Bachelorarbeit\\5_Bachelorarbeit\\5_Version_data_programs_etc\\Programs\\rcx\\standard_setup_long.rcx")
# todo: change to standard_setup short.rcx to play the commented freefield.write and play commands
path_button_rcx = Path("C:\\projects\\Maik Kuerschner\\Biologie Bachelor\\Bachelorarbeit\\Testing Programs\\rcx\\button.rcx")
proc_list = [['RP2', 'RP2', path_button_rcx],
             ['RX81', 'RX8', path_play_buf_rcx],
             ['RX82', 'RX8', path_play_buf_rcx]]
#freefield.initialize_setup(setup="dome", default="loctest_freefield") #not working?

freefield.initialize('dome', device=proc_list)

samplerate = 48828
pinknoise = slab.Sound.pinknoise(duration=1.0, samplerate=samplerate, level=90)
pinknoise_data = pinknoise.data
pinknoise_mod = pinknoise.am(frequency=20)


speakers_coordinates = [(0, 0), (35, 0)]
[speaker1] = freefield.pick_speakers((speakers_coordinates[1]))
# freefield.write('playbuflen', pinknoise.n_samples, ['RX81', 'RX82'])
# freefield.write('data', pinknoise_data, ['RX81', 'RX82'])
# freefield.write('channel', speaker1.analog_channel, speaker1.analog_proc)
# processors = ['RX81', 'RX82']
# processors.remove(speaker1.analog_proc)
# freefield.write('channel', 25, processors)
# freefield.play(kind='zBusA')


duration = 10
total_trials = 10
n_trials_target = int((duration * 20) / 100)
n_trials_default = int(total_trials - n_trials_target)
pink_seq = ['pink'] * n_trials_default
pink_am_seq = ['pink_am'] * n_trials_target
sequence1 = np.concatenate((pink_seq, pink_am_seq))
sequence1 = sequence1.tolist()
np.random.shuffle(sequence1)

sequence1_indices = []
sequence1_labels = []
sounds_sequence1 = []

for index, noise in enumerate(sequence1):
    sequence1_indices.append(index)
    sequence1_labels.append(noise)
    if noise == 'pink':
        sounds_sequence1.append(pinknoise)
    elif noise == 'pink_am':
        sounds_sequence1.append(pinknoise_mod)

precomputed_seq1 = slab.Precomputed(sounds_sequence1)


filter = speaker1.filter

for sounds in precomputed_seq1:
    filter.apply(sounds)

flattened_precomputed_seq1 = np.concatenate([sound.data.flatten() for sound in precomputed_seq1])

sequence1_indices = np.array(sequence1_indices).astype('int32')
sequence1_indices = np.append(0, sequence1_indices)

freefield.write('noise_data', flattened_precomputed_seq1, ['RX81', 'RX82']) # correct
freefield.write('noise_n_samples', int(flattened_precomputed_seq1.size / len(precomputed_seq1)), ['RX81', 'RX82']) # correct
freefield.write('noise_size', flattened_precomputed_seq1.size, ['RX81', 'RX82']) # correct
freefield.write('n_trials', total_trials + 1, ['RX81', 'RX82'])
freefield.write('sequence', sequence1_indices, ['RX81', 'RX82'])
freefield.write('channel', speaker1.analog_channel, speaker1.analog_proc)
processors = ['RX81', 'RX82']
processors.remove(speaker1.analog_proc)
freefield.write('channel', 25, processors)
freefield.play(kind='zBusA')