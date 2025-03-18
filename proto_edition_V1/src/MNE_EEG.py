from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import ttest_rel

import mne

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'


class MNE_EEG:

    def run_mustertest():

        #____LOAD_RAW_DATA____#:
        data_path = mne.datasets.ssvep.data_path()
        bids_fname = data_path / "sub-02" / "ses-01" / "eeg" / "sub-02_ses-01_task-ssvep_eeg.vhdr"
            # path vhdr
        raw = mne.io.read_raw_brainvision(bids_fname, preload = True, verbose = False)
        raw.info["line_freq"] = 50.0
            # Wechelspannungs-Wert


        #____SET_MONTAGE____#:
        montage = mne.channels.make_standard_montage("easycap-M1")
        raw.set_montage(montage, verbose = False)


        #____SET_COMMON_AVERAGE_REFERENCE____#:
        raw.set_eeg_reference("average", projection = False, verbose = False)


        #____APPLY_BANDPASS_FILTER____#:
        raw.filter(l_freq = 0.1, h_freq = None, fir_design = "firwin", verbose = False)
            # high pass


        #____CONSTRUCT_EPOCHS____#:
        raw.annotations.rename({"Stimulus/S255" : "12hz", "Stimulus/S155" : "15hz"})
        epochs = mne.Epochs(
            raw,
            event_id = ["12hz", "15hz"],
            tmin = -1.0,
            tmax = 20.0,
            baseline = None,
            verbose = False
        )

def eigeneEEG():
    raw.annotations.rename({ "XXX" : "zBus", "YYY" : "Button"})
        # insert real Stimulus names from BrainVision Recorder !
    epochs = mne.Epochs(
        raw,
        event_id = ["zBus"] # epochs should only be based on zBus, not buttons !
        tmin = 2.0,         # some dalay after zBus might be beneficial
        tmax = 124-1,       # if 2 min; dropping last second might be safer
        #baseline?
        verbose = False
    )

    #CAVE: drop epochs:  0. and 1. subblock
