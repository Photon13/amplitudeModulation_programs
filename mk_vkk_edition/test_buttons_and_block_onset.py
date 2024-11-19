import freefield
import slab
from pathlib import Path
import numpy as np
import random
from typing import List
from datetime import datetime
import time
#_____________________________________________________________________________________________________
n_subblocks = int(1+30)
n_blocks = int(2 + (4*4)) # 2 training blocks (1 single speaker, 1 both speakers), 4 normal blocks for each condition
#_____________________________________________________________________________________________________

    
""" get rcx files"""
path_play_buf_rcx = Path ("C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\amplitudeModulation_programs\\mk_vkk_edition\\standard_setup_long.rcx")
path_button_rcx = Path ("C:\\projects\\Maik_R_F_K\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\amplitudeModulation_programs\\mk_vkk_edition\\9_buttons.rcx")

proc_list = [['RP2', 'RP2', path_button_rcx],
                 ['RX81', 'RX8', path_play_buf_rcx],
                 ['RX82', 'RX8', path_play_buf_rcx]]
#__________________________________________________________
    
""" initalise processors """
freefield.initialize('dome', device=proc_list)
#__________________________________________________________
n_blocks = 2
blockOnsetsList = ["block_nr | onset_time"] # start entry

# TO ADD: prepare JSON
#___________________________________________________________
for i in range (0, n_blocks+1, 1):

    while True:
        startInput = input(" \n Start block? yes/no: ")
        if startInput.lower() == "yes":
            break
    
    block_nr = i
    buttonArray = [f"block_{block_nr}"]
    buttonTimeArray = [f"block_{block_nr}"]

    # TO ADD: load data onto speakers and leds
    
    freefield.play(kind='zBusA') # trigger for block onset
    # should be sent directly to EEG
    # so following lines might be abundant but helpful for analysis of behavioral data
    blockOnsetsList = blockOnsetsList + [f"block_{block_nr}"]
    block_onset = datetime.datetime.now()
    block_onset = block_onset.strftime("(%H:%M:%S.%f)")
    blockOnsetsList = blockOnsetsList + [f"{block_onset}"]

    stopTime = time.time() + 124 # 124 seconds from now
    while True: # for whole block
        freefield.wait_for_button() # while loop that will break if button pressed 
        
        buttonArray = buttonArray + f"{freefield.read("response", "RP2")}" # appends number of key pressed
        
        timeButtonPress = datetime.datetime.now()
        timeButtonPress = timeButtonPress.strftime("(%H:%M:%S.%f)")
        buttonTimeArray = buttonTimeArray + f"{timeButtonPress}" # appends time of button press event
        
        if time.time() > stopTime:
            break # breaks loop 4 minutes after start loop
    
    # TO ADD: append both lists 
    #   buttonArray
    #   buttonTimeArray
    #   at JSON

# TO ADD: after all blocks finished
# append list blockOnsetsList to (other?) Json
    

    

