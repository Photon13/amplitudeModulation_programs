from Globals import Globals
from Paths import Paths

from pathlib import Path
import mne
import typing
import numpy as np
import matplotlib.pyplot as plt

class mne_test:

    identifier : str = "maik_pilot0"

    A1 = str(32+7) # yellow 7
    A2 = str(32+8) # yellow 8
    # or the other way around
    Cz = str(32+3) # yellow 3

    extension_header : str = ".vhdr"
    extension_marker : str = ".vmrk"
    PATH_RAW : Path = Path(Paths.PATH_FOLDER_BRAINVISION_RECORDER / "rohDaten") 


    def snr_spectrum(psd, noise_n_neighbor_freqs=1, noise_skip_neighbor_freqs=1):
        """Compute SNR spectrum from PSD spectrum using convolution.

        Parameters
        ----------
        psd : ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
            Data object containing PSD values. Works with arrays as produced by
            MNE's PSD functions or channel/trial subsets.
        noise_n_neighbor_freqs : int
            Number of neighboring frequencies used to compute noise level.
            increment by one to add one frequency bin ON BOTH SIDES
        noise_skip_neighbor_freqs : int
            set this >=1 if you want to exclude the immediately neighboring
            frequency bins in noise level calculation

        Returns
        -------
        snr : ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
            Array containing SNR for all epochs, channels, frequency bins.
            NaN for frequencies on the edges, that do not have enough neighbors on
            one side to calculate SNR.
        """
        # Construct a kernel that calculates the mean of the neighboring
        # frequencies
        averaging_kernel = np.concatenate((
            np.ones(noise_n_neighbor_freqs),
            np.zeros(2 * noise_skip_neighbor_freqs + 1),
            np.ones(noise_n_neighbor_freqs)))
        averaging_kernel /= averaging_kernel.sum()

        # Calculate the mean of the neighboring frequencies by convolving with the
        # averaging kernel.
        mean_noise = np.apply_along_axis(
            lambda psd_: np.convolve(psd_, averaging_kernel, mode='valid'),
            axis=-1, arr=psd
        )

        # The mean is not defined on the edges so we will pad it with nas. The
        # padding needs to be done for the last dimension only so we set it to
        # (0, 0) for the other ones.
        edge_width = noise_n_neighbor_freqs + noise_skip_neighbor_freqs
        pad_width = [(0, 0)] * (mean_noise.ndim - 1) + [(edge_width, edge_width)]
        mean_noise = np.pad(
            mean_noise, pad_width=pad_width, constant_values=np.nan
        )

        return psd / mean_noise
    



file_rawHeader = Path(mne_test.PATH_RAW / f"maik_pilot0.vhdr")
raw = mne.io.read_raw_brainvision(file_rawHeader, preload = True, verbose = False)

raw.info["line_freq"] = 50.0

#montage = mne.channels.make_standard_montage("standard_1020") ########
#raw.set_montage(montage, verbose = False)

print(raw.ch_names)
# original:
# "35": "AF4"     "14": "Cz"
# "39": "F2"      "67": "A1"
# "40": "F6"      "65": "A2"

mapping = {
    '35': 'Cz', '14' : 'AF4',
    '39': 'A1', 
    '40': 'A2', 
}
raw.rename_channels(mapping)


raw.filter(l_freq = 0.1, h_freq = None, fir_design = "firwin", verbose = False)
# ? raw.filter.notch_filter(freqs = [50.0])

picks = ['Cz', 'A1', 'A2']
raw.pick_channels(picks)
raw.set_eeg_reference(ref_channels = ['A1', 'A2'])



#____CONSTRUCT_EPOCHS____#:
raw.annotations.rename({
    "Stimulus/S 32" : "shift left", 
    "Stimulus/S  2" : "shift middle",
    "Stimulus/S  1" : "shift right",
    "Stimulus/S 65" : "zBus",
    "Stimulus/S128" : "button"
})


###################
raw.plot(clipping = None) # seems to work ? # but why 3 channels shown?
inp = input("Type something: ") 
####################


# bad epochs
epochs = mne.Epochs(
    raw,
    event_id = ["zBus"],
    tmin = +1.0,
    tmax = +39.5,
    baseline = None,
    picks = picks,
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
psds, freqs = spectrum.get_data(return_freqs = True)

#____CALC_SIGNAL_TO_NOISE_SPECTRUM____#:
snrs = mne_test.snr_spectrum(psds, noise_n_neighbor_freqs = 3, noise_skip_neighbor_freqs = 1)    

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
axes[1].plot(freqs[freq_range], snr_mean, color = "r")
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
inp = input(" Type something: ")