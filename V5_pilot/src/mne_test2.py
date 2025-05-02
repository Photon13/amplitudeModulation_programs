import matplotlib.pyplot as plt
from pathlib import Path
import mne
from typing import List
import numpy as np
import sys
import pandas as pd

from Paths import Paths

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'


@staticmethod
def plotAllEvents_inRaw(rawBV, events : np.ndarray, event_id : dict):
    mne.viz.plot_events(events = events, event_id = event_id, sfreq = rawBV.info["sfreq"])
    # <marker name> (<nr>) : <nr> is number of occurrences marker
    # sfreq == sample frequency
    inp = input("Continue? [any]: ")

@staticmethod
def get_eventIdDict(eventType):
    """ eventTypes == "all" | "zBus" | "buttonsAndShifts" """
    if( eventType == "all"):
        return {
        "StartRecording" : 99999,
        "shiftLeft" : 32, 
        "shiftMiddle" : 2,
        "shiftRight" : 1,
        "zBus" : 65,
        "button" : 128
        }
    elif( eventType == "zBus"):
        return {
        "zBus" : 65
        }
    elif( eventType == "buttonsAndShifts"):
        return {
        "shiftLeft" : 32, 
        "shiftMiddle" : 2,
        "shiftRight" : 1,
        "button" : 128
        }
    else:
        print(COLORRED + "Invalid eventType!" + COLOREND)
        sys.exit()



pathRaw : Path = Path(Paths.PATH_FOLDER_BRAINVISION_RECORDER / "rohDaten" / f"maik_pilot0.vhdr" )
rawBV = mne.io.read_raw_brainvision(pathRaw, preload = True, verbose = False)

# FILTERING
rawBV.filter(l_freq = 20, h_freq = 60)
rawBV.info["line_freq"] = 50.0


# RENAMING ANNOTATIONS: "Stimulus/S 32" into "shiftLeft" etc.
rawBV.annotations.rename({
    "New Segment/" : "StartRecording",
    "Stimulus/S 32" : "shiftLeft", 
    "Stimulus/S  2" : "shiftMiddle",
    "Stimulus/S  1" : "shiftRight",
    "Stimulus/S 65" : "zBus",
    "Stimulus/S128" : "button"
})
# rawBV.annotations == <Annotations | 322 segments: StartRecording/ (1), shiftLeft (95), ...>
# number in brackets is respective number of occurrences marker



allEvents, allEvent_id = mne.events_from_annotations(
    raw = rawBV, 
    event_id = {
        "StartRecording" : 99999,
        "shiftLeft" : 32, 
        "shiftMiddle" : 2,
        "shiftRight" : 1,
        "zBus" : 65,
        "button" : 128
        }
)
# plotAllEvents_inRaw(rawBV, allEvents, allEvent_id)



zBusEvents, zBusEvent_id = mne.events_from_annotations(
    raw = rawBV, 
    event_id = {
        "zBus" : 65
        }
)

nrCurrentBlock = 0
start_blockX = zBusEvents[nrCurrentBlock][2] /rawBV.info["sfreq"]
end_blockX = start_blockX + 40
rawBV_blockX = rawBV.copy().crop(tmin = start_blockX, tmax = end_blockX, include_tmax = False)
# (drop last sec)  
###### The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

buttonsAndShiftsEvents_blockX, buttonsAndShiftsEvents_blockX_id = mne.events_from_annotations(
    raw = rawBV_blockX, 
    event_id = {
        "shiftLeft" : 32, 
        "shiftMiddle" : 2,
        "shiftRight" : 1,
        "button" : 128
        }
)


epochs_bockX = mne.Epochs(rawBV_blockX, buttonsAndShiftsEvents_blockX)
#Exception has occurred: TypeError
#events should be a NumPy array of integers, got <class 'tuple'>
#ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (2,) + inhomogeneous part.

metadata_buttonsAndShiftsEvents_blockX : pd.DataFrame = mne.epochs.make_metadata(
    events = buttonsAndShiftsEvents_blockX,
    event_id = buttonsAndShiftsEvents_blockX_id,
    tmin = 0.0,
    tmax = 1.5,
    sfreq = rawBV.info["sfreq"],
    row_events = ["shiftLeft", "shiftMiddle", "shiftRight"]
)[0]
print(metadata_buttonsAndShiftsEvents_blockX)

buttonDict_blockX = metadata_buttonsAndShiftsEvents_blockX.to_dict(orient = "list")
print(buttonDict_blockX)

#blockX_button_presses : List(tuple(str, float)) = []
#for i in range( len(metadata_buttonsAndShiftsEvents_blockX)):
#    if( metadata_buttonsAndShiftsEvents_blockX[i]):


