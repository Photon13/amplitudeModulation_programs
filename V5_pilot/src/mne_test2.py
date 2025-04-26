import matplotlib.pyplot as plt
from pathlib import Path
import mne
from typing import List
import numpy as np

from Paths import Paths



@staticmethod
def plotAllEvents_inRaw(rawBV, events : np.ndarray, event_id : dict):
    mne.viz.plot_events(events = events, event_id = event_id, sfreq = rawBV.info["sfreq"])
    # <marker name> (<nr>) : <nr> is number of occurrences marker
    # sfreq == sample frequency
    inp = input("Continue? [any]: ")


@staticmethod
def get_events():
    allEvents = mne.events_from_annotations(
        raw = rawBV, 
        event_id = {
        "StartRecording" : 99999,
        "shiftLeft" : 32, 
        "shiftMiddle" : 2,
        "shiftRight" : 1,
        "zBus" : 65,
        "button" : 128
        }
    )[0]

    shiftButtonEvents = mne.events_from_annotations(
        raw = rawBV, 
        event_id = {
        "shiftLeft" : 32, 
        "shiftMiddle" : 2,
        "shiftRight" : 1,
        "button" : 128
        }
    )[0]
    # shiftButtonEvents == [[ 10613      0      1] [ 11613      0      1] ... ]

    zBusEvents = mne.events_from_annotations(
        raw = rawBV, 
        event_id = {
        "zBus" : 65
        }
    )[0]
    return allEvents, shiftButtonEvents, zBusEvents




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

allEvents, shiftButtonEvents, zBusEvents = get_events()


#plotAllEvents_inRaw(rawBV, allEvents, allEvent_id)


metadata_shiftButtonEvents = mne.epochs.make_metadata(
    events = shiftButtonEvents,
    event_id = {
        "shiftLeft" : 32, 
        "shiftMiddle" : 2,
        "shiftRight" : 1,
        "button" : 128
        },
    tmin = 0.0,
    tmax = 2.0,
    sfreq = rawBV.info["sfreq"],
    row_events = ["shiftLeft", "shiftMiddle", "shiftRight"]
)[0]
print(metadata_shiftButtonEvents)





dictBlockData : dict = {}
for i in range(0, 19, 2): # n blocks total for pilot maik == 20
    blockNr = i
    tmin = timePointsZBus[blockNr] / rawBV.info["sfreq"] # sec
    tmax = tmin + 40 # sec
    rawBV_block = rawBV.crop(tmin = tmin, tmax = tmax, include_tmax = True)
    

    blockData = [metadata, events_block, event_id_block]
    dictBlockData[f"block{blockNr}"] = blockData
print(dictBlockData)
