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


@staticmethod
def loop_trough_blocks(nrCurrentBlock, rawBV):

    start_blockX = zBusEvents[nrCurrentBlock][2] /rawBV.info["sfreq"]
    end_blockX = start_blockX + 40
    rawBV_blockX = rawBV.copy().crop(tmin = start_blockX, tmax = end_blockX, include_tmax = True)


    buttonsAndShiftsEvents_blockX, buttonsAndShiftsEvents_blockX_id = mne.events_from_annotations(
        raw = rawBV_blockX, 
        event_id = {
            "zBus" : 65,
            "shiftLeft" : 32, 
            "shiftMiddle" : 2,
            "shiftRight" : 1,
            "button" : 128
            }
    )
    print(COLORBLUE + f"{buttonsAndShiftsEvents_blockX}" + COLOREND)


    epochs_bockX = mne.Epochs(rawBV_blockX, buttonsAndShiftsEvents_blockX)

    df_shifts_blockX : pd.DataFrame = mne.epochs.make_metadata(
        events = buttonsAndShiftsEvents_blockX,
        event_id = buttonsAndShiftsEvents_blockX_id,
        tmin = 0.0, # for including zBus
        tmax = 39.7,
        sfreq = rawBV.info["sfreq"],
        row_events = ["zBus", "shiftLeft", "shiftMiddle", "shiftRight"]
    )[0]
    print(df_shifts_blockX)


    df_buttons_blockX : pd.DataFrame = mne.epochs.make_metadata(
        events = buttonsAndShiftsEvents_blockX,
        event_id = buttonsAndShiftsEvents_blockX_id,
        tmin = 0.0,
        tmax = 1.5,
        sfreq = rawBV.info["sfreq"],
        row_events = ["shiftLeft", "shiftMiddle", "shiftRight"]
    )[0]
    print(df_buttons_blockX)

    buttonDict_blockX = df_buttons_blockX.to_dict(orient = "list")
    print(buttonDict_blockX)

    shiftLeftButton_blockX : List[float] = [] # relative (!) time points
    shiftMiddleButton_blockX : List[float] = []
    shiftRightButton_blockX : List[float] = []

    for i in range( len(buttonDict_blockX["button"]) ):
        if( np.isnan(buttonDict_blockX["button"][i]) == False ):
            if( buttonDict_blockX["event_name"][i] == "shiftLeft" ):
                shiftLeftButton_blockX.append( buttonDict_blockX["button"][i] ) # relative (!) time points
            elif( buttonDict_blockX["event_name"][i] == "shiftMiddle" ):
                shiftMiddleButton_blockX.append( buttonDict_blockX["button"][i] )
            elif( buttonDict_blockX["event_name"][i] == "shiftRight" ):
                shiftRightButton_blockX.append( buttonDict_blockX["button"][i] )
            else:
                print( COLORRED + "Invalid entry in shift<position>_blockX" + COLOREND + "Message from for-loop buttonDict_blockX.")


    return buttonsAndShiftsEvents_blockX, shiftLeftButton_blockX, shiftMiddleButton_blockX, shiftRightButton_blockX







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

blockDict = {}

for i in range(0,2):
    currentBlockNr = i
    blockDict[f"block{currentBlockNr}"] = [loop_trough_blocks(currentBlockNr, rawBV)]
    # buttonsAndShiftsEvents_blockX, shiftLeftButton_blockX, shiftMiddleButton_blockX, shiftRightButton_blockX = loop_trough_blocks(currentBlockNr, rawBV)
    # time points of shifts relative to zBus; time points button relative to shift in 1.5 sec time window after shift

print(blockDict)




