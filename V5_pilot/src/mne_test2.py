import matplotlib.pyplot as plt
from pathlib import Path
import mne

from Paths import Paths

pathRaw : Path = Path(Paths.PATH_FOLDER_BRAINVISION_RECORDER / "rohDaten" / f"maik_pilot0.vhdr" )

rawBV = mne.io.read_raw_brainvision(pathRaw, preload = True, verbose = False)

rawBV.filter(l_freq = 20, h_freq = 60)
rawBV.info["line_freq"] = 50.0

annotationDict = ({
    "Stimulus/S 32" : "shiftLeft", 
    "Stimulus/S  2" : "shiftMiddle",
    "Stimulus/S  1" : "shiftRight",
    "Stimulus/S 65" : "zBus",
    "Stimulus/S 66" : "failedBlockStart",
    "Stimulus/S128" : "button"
})

rawBV.annotations.rename(annotationDict)

eventDict_nameId = ({
    "shiftLeft" : 32, 
    "shiftMiddle" : 2,
    "shiftRight" : 1,
    "zBus" : 65,
    "failedBlockStart" : 66,
    "button" : 128
})


allEvents, allEvent_id = mne.events_from_annotations(raw = rawBV, event_id = eventDict_nameId)
# allEvents : NDarray[] == [[     0      0  99999] [  7113      0     65] [ 10613      0      1] ... ]
# allEvent_id : dict == {'New Segment/': 99999, 'Stimulus/S  1': 1, 'Stimulus/S  2': 2, 'Stimulus/S 32': 32, 'Stimulus/S 65': 65, 'Stimulus/S 66': 66, 'Stimulus/S128': 128}
print(allEvents)
print(allEvent_id)

mne.viz.plot_events(events = allEvents, event_id = allEvent_id, sfreq = rawBV.info["sfreq"])
# nr behind marker name is number of occurrences
# sfreq == sample frequency
inp = input("Continue? [any]: ")

rowEvents = [
    "shiftLeft", 
    "shiftMiddle",
    "shiftRight",
    "zBus",
    "failedBlockStart",
    "button"
]

occurenceTimes_zBus = [] 
for i in range(len(allEvents)):
    if(allEvents[i][2] == eventDict_nameId["zBus"]):
        # allEvents[i][2] last entry of sub-NDarray
        occurenceTimes_zBus.append(allEvents[i][0])
        # allEvents[i][0] first entry of sub-NDarray
print(occurenceTimes_zBus)
#occurenceTimes_zBus = [7113, 47143, 87170, 130914, 172943, 216291, 259598, 318812, 360714, 405850]

# Continue? [any]: j

blockNr = 0

tmin = occurenceTimes_zBus[blockNr] # change to sec instead of samples?
tmax = tmin + 40
rawBV.crop(tmin = tmin, tmax = tmax, include_tmax = True)
metadata_block0, events_block0, event_id_block0 = mne.epochs.make_metadata(
    events = allEvents,
    event_id = allEvent_id,
    tmin = 0.0,
    tmax = 2.0,
    sfreq = rawBV.info["sfreq"],
    row_events = rowEvents,
)
print(metadata_block0)

# undo renaming 65 -> 66 ! (for addressing per block nr)
