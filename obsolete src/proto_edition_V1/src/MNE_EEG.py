from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import ttest_rel

import mne

import typing

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
        #____CALC_POWER_SPECTRAL_DENSITY____#:
        tmin : float = 1.0
        tmax : float = 20.0
        fmin = 1.0
        fmax = 90.0
        sfreq = epochs.info["sfreq"]
        spectrum = epochs.compute_psd(
            "welch",
            n_fft = int(sfreq*(tmax-tmin)),
            n_overlap = 0,
            n_per_seg = None,
            tmin = tmin,
            tmax = tmax,
            fmin = fmin,
            fmax = fmax,
            window = "boxcar",
            verbose = False
        )
        psds, freqs = spectrum.get_data(return_freq = True)

        #____CALC_SIGNAL_TO_NOISE_SPECTRUM____#:
        snrs = snr_spectrum(psds, noise_n_neighbor_freqs = 3, noise_skip_neigbor_freqs = 1)
        
        #____PLOT_PSD_AND_SNR____#:
        fig, axes = plt.subplots(2, 1, sharex = "all", sharey = "none", figsize = (8,5))
        freq_range = range( np.where(np.floor(freqs) == 1.0)[0][0],
                            np.where(np.ceil(freqs) == fmax-1)[0][0]
                            )
        psds_plot = 10 * np.log10(psds)
        psds_mean = psds_plot.mean(axis=(0,1)) [freq_range]
        psds_std = psds_plot.std(axis=(0,1)) [freq_range]
        axes[0].plot(freqs[freq_range], psds_mean, color = "b")
        axes[0].fill_between(
            freqs[freq_range], 
            psds_mean - psds_std,
            psds_mean + psds_std,
            color = "b",
            alpha = 0.2
        )
        axes[0].set(title = "PSD spectrum", ylabel = "Power Spectral Density [dB]")

        # SNR spectrum
        snr_mean = snrs.mean(axis=(0,1)) [freq_range]
        snr_std = snrs.std(axis=(0,1)) [freq_range]
        axes[1].plot(reqs[freq_range], snr_mean, color = "r")
        axes[1].fill_between(
            freqs[freq_range],
            snr_mean - snr_std,
            snr_mean + snr_std,
            color = "r",
            alpha = 0.2
        )
        axes[1].set(
            title = "SNR spectrum",
            xlabel = "Frequency [Hz]",
            ylabel = "SNR",
            ylim = [-2, 30],
            xlim = [fmin, fmax]
        )
        fig.show()




def eigeneEEG():
    """raw.annotations.rename({ "XXX" : "zBus", "YYY" : "Button"})
        # insert real Stimulus names from BrainVision Recorder !
    epochs = mne.Epochs(
        raw,
        event_id = ["zBus"] # epochs should only be based on zBus, not buttons !
        tmin = 2.0,         # some dalay after zBus might be beneficial
        tmax = 124-1,       # if 2 min; dropping last second might be safer
        #baseline?
        verbose = False
    )

    #CAVE: drop epochs:  0. and 1. subblock"
    """
