import mne
from pathlib import Path
from typing import List

from Globals import Globals

import matplotlib
import sys

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

class EEG_Paths:
    BVR_pathFile : Path = Path(Globals.PATH_FOLDER_BRAINVISION_RECORDER)
    raw_pathFolder : Path = BVR_pathFile / "vrvrakk" / "raw_vrvrakk"
    fif_pathFolder : Path = BVR_pathFile / "vrvrakk" / "zwischen_vrvrakk"

    #vhdr_pathFile : Path = raw_pathFolder / "ad_a1.vhdr"
    #fif_pathFile : Path  = fif_pathFolder / "ad_a1.fif"


class Test:


    def show_rawPlot(): # works

        vhdr_pathFile : Path = EEG_Paths.raw_pathFolder / "ad_a1.vhdr"
        raw = mne.io.read_raw_brainvision(vhdr_pathFile, preload = True) # raw instance is in fif format
        raw.plot(block = True) # block prevents sudden closing of plot
 
    def showConcatenatedRawPlot(): # really slow

        vhdr_pathFile0 : Path = EEG_Paths.raw_pathFolder / "ad_a1.vhdr"
        vhdr_pathFile1 : Path = EEG_Paths.raw_pathFolder / "ad_a1_1.vhdr"
        vhdr_pathFile2 : Path = EEG_Paths.raw_pathFolder / "ad_a1_2.vhdr"
        vhdr_pathFile3 : Path = EEG_Paths.raw_pathFolder / "ad_a1_3.vhdr"
        vhdr_pathFile4 : Path = EEG_Paths.raw_pathFolder / "ad_a1_4.vhdr"

        raw0 = mne.io.read_raw_brainvision(vhdr_pathFile0, preload = True)
        raw1 = mne.io.read_raw_brainvision(vhdr_pathFile1, preload = True) 
        raw2 = mne.io.read_raw_brainvision(vhdr_pathFile2, preload = True) 
        raw3 = mne.io.read_raw_brainvision(vhdr_pathFile3, preload = True)
        raw4 = mne.io.read_raw_brainvision(vhdr_pathFile4, preload = True)   

        raw_fused = mne.concatenate_raws([raw0, raw1, raw2, raw3, raw4])

        raw_downsampled = raw_fused.copy().resample(sfreq=200) # still slow?
        raw_downsampled.plot(block = True)

    def show_rawPlot_withChangedChannelNames(): # returns RawBrainVision      # works
        
        vhdr_pathFile : Path = EEG_Paths.raw_pathFolder / "ad_a1.vhdr"

        raw = mne.io.read_raw_brainvision(vhdr_pathFile, preload = True) # raw instance is in fif format

        electrodeNamesDict : dict = Test.get_electrodeNamesDict()
        raw.rename_channels(electrodeNamesDict)
        raw.drop_channels(['A1', 'A2', 'M2']) # exclude EMG channels

        raw.plot() 
        raw.plot_psd() # power spectral density

        while True: # prevents sudden closing of plot
            inp = input(COLORBLUE + "Quit program? yes: " + COLOREND)
            if inp.lower() == "yes":
                sys.exit()
            else:
                return raw




    def fetch_raw():
        
        vhdr_pathFile : Path = EEG_Paths.raw_pathFolder / "ad_a1.vhdr"
        raw = mne.io.read_raw_brainvision(vhdr_pathFile, preload = True) # raw instance is in fif format
        return raw
    

    def plot_lines(raw) -> None:
        raw.plot(block=True) # prevents sudden closing of plot


    def plot_psd(raw) -> None:
        raw.compute_psd().plot() # power spectral density

        while True: # prevents sudden closing of plot
            inp = input(COLORBLUE + "Continue? yes: " + COLOREND)
            if inp.lower() == "yes":
                return None
    

    def get_electrodeNamesDict() -> dict:
        electrodeNamesDict : dict = {
                "1": "Fp1",
                "2": "Fp2",
                "3": "F7",
                "4": "F3",
                "5": "Fz",
                "6": "F4",
                "7": "F8",
                "8": "FC5",
                "9": "FC1",
                "10": "FC2",
                "11": "FC6",
                "12": "T7",
                "13": "C3",
                "14": "Cz",
                "15": "C4",
                "16": "T8",
                "17": "TP9",
                "18": "CP5",
                "19": "CP1",
                "20": "CP2",
                "21": "CP6",
                "22": "TP10",
                "23": "P7",
                "24": "P3",
                "25": "Pz",
                "26": "P4",
                "27": "P8",
                "28": "PO9",
                "29": "O1",
                "30": "Oz",
                "31": "O2",
                "32": "PO10",
                "33": "AF7",
                "34": "AF3",
                "35": "AF4",
                "36": "AF8",
                "37": "F5",
                "38": "F1",
                "39": "F2",
                "40": "F6",
                "41": "FT9",
                "42": "FT7",
                "43": "FC3",
                "44": "FC4",
                "45": "FT8",
                "46": "FT10",
                "47": "C5",
                "48": "C1",
                "49": "C2",
                "50": "C6",
                "51": "TP7",
                "52": "CP3",
                "53": "CPz",
                "54": "CP4",
                "55": "TP8",
                "56": "P5",
                "57": "P1",
                "58": "P2",
                "59": "P6",
                "60": "PO7",
                "61": "PO3",
                "62": "POz",
                "63": "PO4",
                "64": "PO8",
                "65": "A2",
                "66": "M2",
                "67": "A1"
        }
        return electrodeNamesDict


    def change_electrodeNames(raw):
        electrodeNamesDict : dict = Test.get_electrodeNamesDict()
        raw.rename_channels(electrodeNamesDict)
        raw.drop_channels(['A1', 'A2', 'M2']) # exclude EMG channels
        return raw


    def filter_raw(raw): # Param & Return: RawBrainVision
        raw.filter(l_freq = 2 , h_freq = 70)
        raw.notch_filter(freqs = [50.0]) # Netzspannung?
        return raw
    
    def set_badChannels(raw, badChannels : List[str]): # Param & Return: RawBrainVision
        print(raw.info)
        raw.info["bads"] = badChannels
        return raw

        
    def get_markerDict() -> dict:
        markersDict : dict = {
            's1_events': {  
                'Stimulus/S 1': 1,
                'Stimulus/S 2': 2,
                'Stimulus/S 3': 3,
                'Stimulus/S 4': 4,
                'Stimulus/S 5': 5,
                'Stimulus/S 6': 6,
                'Stimulus/S 8': 8,
                'Stimulus/S 9': 9
            },
            's2_events': {  
                'Stimulus/S 65': 65,
                'Stimulus/S 66': 66,
                'Stimulus/S 67': 67,
                'Stimulus/S 68': 68,
                'Stimulus/S 69': 69,
                'Stimulus/S 70': 70,
                'Stimulus/S 72': 72,
                'Stimulus/S 73': 73
            },
            'response_events': {  
                'Stimulus/S129': 129,
                'Stimulus/S130': 130,
                'Stimulus/S131': 131,
                'Stimulus/S132': 132,
                'Stimulus/S133': 133,
                'Stimulus/S134': 134,
                'Stimulus/S136': 136,
                'Stimulus/S137': 137
            }
        }
        return markersDict


#__________________________________

raw = Test.fetch_raw()
raw = Test.change_electrodeNames(raw)
raw = Test.filter_raw(raw)

Test.plot_lines(raw)

#__________________________________




#_________________________________

### re-referencing should be unnecessary

#raw_mastoid = raw.copy().set_eeg_reference(ref_channels=['M1', 'M2']) # Mastoid average, not available in vrvrakk's files


#raw_cz_ref = raw.copy().set_eeg_reference(ref_channels=['Cz'])
#Test.plot_lines(raw_cz_ref)

#raw_average_ref = raw.copy().set_eeg_reference(ref_channels="average")
#Test.plot_lines(raw_average_ref)

#_________________________________




#__________________________________

# following code seems to work

channelsToInterpolate : List[str]= ["T8"] # CHANGE ! ! !
raw = Test.set_badChannels(raw, channelsToInterpolate)
raw.set_montage('standard_1020')
raw.interpolate_bads(reset_bads=False) # function needs montage for interpolation

# save <participant>.excluded_channels
# and <participant>.interpolated_channels
# load json, re-write and save (should be able to be done changed again, if necessary)

channelsToExclude : List[str] = []
raw = Test.set_badChannels(raw, channelsToExclude)

#____________________________________




#____________________________________

Test.plot_lines(raw) # use if clicking on line shall not have an effect (returns None)
Test.plot_psd(raw)
#____________________________________





#____________________________________

# ?

markerDict : dict = Test.get_markerDict()
s1_events = markerDict['s1_events']
s2_events = markerDict['s2_events']  # stimulus 2 markers
response_events = markerDict['response_events']  # response markers

#____________________________________




#____________________________________
#?

#raw_fif = mne.io.read_raw_fif(fif_pathFile) #?



