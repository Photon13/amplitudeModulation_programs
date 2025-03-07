#import freefield
#from pathlib import Path

#path_play_buf_rcx = Path(
#    "C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\amplitudeModulation_programs\\mk_vkk_edition\\standard_setup_long_5.rcx"
#)
#path_button_rcx = Path(
#    "C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\amplitudeModulation_programs\\mk_vkk_edition\\button.rcx"
#)
#proc_list = [['RP2', 'RP2', path_play_buf_rcx],
#             ['RX81', 'RX8', path_play_buf_rcx],
#             ['RX82', 'RX8', path_play_buf_rcx]]

#freefield.initialize('dome', device=proc_list)



#led_coordinates = [(0, 50), (0, 25), (0,0), (0,-25), (0, -50)]
#led_coordinates = [(19), (21), (23), (25), (27)]

#[led_19] = freefield.pick_speakers((led_coordinates[0])) #bit0, supertop (speaker19)
#[led_21] = freefield.pick_speakers((led_coordinates[1])) #bit2 top (speaker21) ##rcx digital_channel: 4
#[led_23] = freefield.pick_speakers((led_coordinates[2])) #bit3 centre (speaker23) ##rcx digital_channel: 8
#[led_25] = freefield.pick_speakers((led_coordinates[3])) #bit4 centre (speaker25) ## rcx digital_channel: 16
#[led_27] = freefield.pick_speakers((led_coordinates[4])) #nix (sic!) -> must be bit-64 on rcx

#print(freefield.all_leds())

#________________________________________________________________________
"""obsolet"""
#freefield.write('bitmask', led_19.digital_channel, led_19.digital_proc)
#freefield.write('bitmask', led_21.digital_channel, led_21.digital_proc)
#freefield.write('bitmask', led_23.digital_channel, led_23.digital_proc)
#freefield.write('bitmask', led_25.digital_channel, led_25.digital_proc)
#freefield.write('bitmask', led_27.digital_channel, led_27.digital_proc)

#freefield.write('bitmask', 0, led_19.digital_proc)
#freefield.write('bitmask', 0, led_21.digital_proc)
#freefield.write('bitmask', 0, led_23.digital_proc)
#freefield.write('bitmask', 0, led_25.digital_proc)
#freefield.write('bitmask', 0, led_27.digital_proc)
#_______________________________________________________________________
#led_coordinates = [(0, 25), (0,50), (0,-25)]

#[led_21] = freefield.pick_speakers((led_coordinates[0])) #bit2 top (speaker21) ##rcx digital_channel: 4 #2^2
#[led_23] = freefield.pick_speakers((led_coordinates[1])) #bit3 centre (speaker23) ##rcx digital_channel: 8 #2^3
#[led_25] = freefield.pick_speakers((led_coordinates[2])) #bit4 centre (speaker25) ## rcx digital_channel: 16 #2^4

#freefield.write('bitmaskLeft', led_21.digital_channel, led_21.digital_proc)
#freefield.write('bitmaskMiddle', led_23.digital_channel, led_23.digital_proc)
#freefield.write('bitmaskRight', led_25.digital_channel, led_25.digital_proc)

#freefield.write('bitmaskLeft', 0, led_21.digital_proc)
#freefield.write('bitmaskMiddle', 0, led_23.digital_proc)
#freefield.write('bitmaskRight', 0, led_25.digital_proc)

#19+23->nur 23 leuchtet
#23+19->nur 19 leuchtet

#21+23-> nur 23 leuchtet
#23+21-> nur 21 leuchtet

#23+25 -> nur 25 leuchtet
#25+23-> nur 23 leuchtet

#_______________________________________________________________________
import freefield
from pathlib import Path

PATH_RCX_FILE = Path("C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\amplitudeModulation_programs\\proto_edition_V1\\data\\rcx\\standard_setup_long_pre_final.rcx")

proc_list = [['RP2', 'RP2', PATH_RCX_FILE],
             ['RX81', 'RX8', PATH_RCX_FILE],
             ['RX82', 'RX8', PATH_RCX_FILE]]

freefield.initialize('dome', device=proc_list)

LED_COORDINATES = [(0, -25), (0, 0), (0, 25)]

[ledLeft] = freefield.pick_speakers(LED_COORDINATES[0])
[ledMiddle] = freefield.pick_speakers(LED_COORDINATES[1])
[ledRight] = freefield.pick_speakers(LED_COORDINATES[2])



freefield.write("bitmaskLeft", ledLeft.digital_channel, ledLeft.digital_proc)
freefield.write( "bitmaskMiddle", ledMiddle.digital_channel, ledRight.digital_proc)
freefield.write("bitmaskRight", ledRight.digital_channel, ledRight.digital_proc)

#freefield.write("bitmaskLeft", 0, ledLeft.digital_proc)
#freefield.write("bitmaskMiddle", 0, ledMiddle.digital_proc)
#freefield.write("bitmaskRight", 0, ledRight.digital_proc)