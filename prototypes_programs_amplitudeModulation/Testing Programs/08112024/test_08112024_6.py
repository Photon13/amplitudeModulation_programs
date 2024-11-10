import freefield
import slab
from pathlib import Path
#________________________________________________________________________
path_rcx = Path (
    "C:\\projects\\Maik Kuerschner\\Biologie Bachelor\\Bachelorarbeit\\test_08112024_3\\rcx\\"
)
path_circuit_R2 = path_rcx / "button.rcx"
path_circuit_RX8 = path_rcx / "maik_circuit_08112024_5.rcx"

print(path_circuit_R2)
print(path_circuit_RX8)
#________________________________________________________________________
proc_list = [
    ['RP2', 'RP2', path_circuit_R2],
    ['RX81', 'RX8', path_circuit_RX8],
    ['RX82', 'RX8', path_circuit_RX8]
]

freefield.initialize('dome', device = proc_list)

#________________________________________________________________________
# (azimuth, elevation) ## [left, middle, right]
speaker_coordinates = [(-35,0), (0,0), (35,0)]

[speakerLeft] = freefield.pick_speakers (
    (speaker_coordinates [0])
)

[speakerMiddle] = freefield.pick_speakers (
    (speaker_coordinates [1])
)

[speakerRight] = freefield.pick_speakers (
    (speaker_coordinates [2])
)

#________________________________________________________________________
print(freefield.all_leds())
# (azimuth, elevation) ## [left, middle, right] ### actually: [down, middle, up]
led_coordinates = [(21), (23), (25)]


[ledLeft] = freefield.pick_speakers (
    (led_coordinates [0])
)

[ledMiddle] = freefield.pick_speakers (
    (led_coordinates [1])
)

[ledRight] = freefield.pick_speakers (
    (led_coordinates [2])
)
#print(speakerLeft.analog_channel) # 1
#print(speakerMiddle.analog_channel) #1
#print(speakerRight.analog_channel) #23

print(ledLeft.digital_channel) #None
print(ledMiddle.digital_channel) #None
print(ledRight.digital_channel) #None

#________________________________________________________________________
samplerate = 44100 # n samples = duration * samplerate
level = 70

duration = float(20.0) # duration_sound_left == duration_sound_middle == duration_sound_right
n_samples = int(duration * samplerate)
#________________________________________________________________________
freq_am_soundLeft = 20

soundLeft = slab.Sound.pinknoise (
    duration, samplerate, level
    )
soundLeft = soundLeft.am (
    freq_am_soundLeft, 1.0
    )
#________________________________________________________________________
freq_am_soundMiddle = 1

soundMiddle = slab.Sound.pinknoise (
    duration, samplerate, level
    )
soundMiddle = soundMiddle.am (
    freq_am_soundMiddle
    )
#________________________________________________________________________
freq_am_soundRight = 50

soundRight = slab.Sound.pinknoise (
    duration, samplerate, level
    )
soundRight = soundRight.am (
    freq_am_soundRight
    )
#________________________________________________________________________
freefield.write(
    'playbuflen', n_samples, ['RX81', 'RX82']
)
freefield.write(
    'dataLeft', soundLeft.data, speakerLeft.analog_proc
)
freefield.write(
    'channelLeft', speakerLeft.analog_channel, speakerLeft.analog_proc
)

other_proc = ['RX81', 'RX82']
other_proc.remove (speakerLeft.analog_proc)
#print(f"{soundLeft.n_samples}")
print(other_proc)

freefield.write(
    'channelLeft', 99, other_proc
)
#________________________________________________________________________
freefield.write( #only needed once?
    'playbuflen', n_samples, ['RX81', 'RX82']
)
freefield.write(
    'dataMiddle', soundMiddle.data, speakerMiddle.analog_proc
)
freefield.write(
    'channelMiddle', speakerMiddle.analog_channel, speakerMiddle.analog_proc
)

other_proc = ['RX81', 'RX82']
other_proc.remove (speakerMiddle.analog_proc)

print(other_proc)

freefield.write(
    'channelMiddle', 99, other_proc
)
#________________________________________________________________________
freefield.write(
    'playbuflen', n_samples, ['RX81', 'RX82']
)
freefield.write(
    'dataRight', soundRight.data, speakerRight.analog_proc
)
freefield.write(
    'channelRight', speakerRight.analog_channel, speakerRight.analog_proc
)

other_proc = ['RX81', 'RX82']
other_proc.remove (speakerRight.analog_proc)

print(other_proc)

freefield.write(
    'channelRight', 99, other_proc
)
#________________________________________________________________________
#puffer?
freefield.write('bitmask', ledLeft.digital_channel, ledLeft.digital_proc)
freefield.write('bitmask', ledMiddle.digital_channel, ledMiddle.digital_channel)
freefield.write('bitmask', ledRight.digital_channel. ledRight.digital_proc)
#________________________________________________________________________
freefield.play()

#warten

#freefield.write("bitmask", 0, ledLeft.digital_proc)
#freefield.write("bitmask", 0, ledMiddle.digital_proc)
#freefield.write("bitmask", 0, ledRight.digital_proc)

#freefield.halt() # undo initializing