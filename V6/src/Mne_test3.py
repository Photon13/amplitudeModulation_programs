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

class MneTestMaik:

    @staticmethod
    def get_prepared_rawBV():

        pathRaw : Path = Path(Paths.PATH_FOLDER_BRAINVISION_RECORDER / "rohDaten" / f"maik_pilot0.vhdr" )
            # get file path
        rawBV = mne.io.read_raw_brainvision(pathRaw, preload = True, verbose = False)
            # load data from raw file

        rawBV.filter(l_freq = 20, h_freq = 60)
            # apply low-pass and high-pass filtering
        rawBV.info["line_freq"] = 50.0
            # define line frequency

        rawBV.annotations.rename({
            "New Segment/" : "StartRecording",
            "Stimulus/S 32" : "shiftLeft", 
            "Stimulus/S  2" : "shiftMiddle",
            "Stimulus/S  1" : "shiftRight",
            "Stimulus/S 65" : "zBus",
            "Stimulus/S128" : "button"
        })
            # rename annotatons: "Stimulus/S 32" into "shiftLeft" etc.
        return rawBV
    

    @staticmethod
    def get_allEvents(rawBV):
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
        return allEvents, allEvent_id



    @staticmethod
    def plot_allMarkers(rawBV) -> None:
        allEvents, allEvent_id = MneTestMaik.get_allEvents(rawBV)
        mne.viz.plot_events(allEvents, allEvent_id, sfreq = rawBV.info["sfreq"])
        inp = input("Continue? [any]: ")

        # allEvents == [[     0      0  99999] [  7113      0     65] ...]



    @staticmethod
    def get_tSampList_markers(typeOfMarker : str, rawBV) -> List[int]:
        match typeOfMarker:
            case "zBus":
                identifier = 65
            case "shiftLeft":
                identifier = 32
            case "shiftMiddle":
                identifier = 2
            case "shiftRight":
                identifier = 1
            case "button":
                identifier = 128
            case _:
                print( COLORRED + "Invalid type in get_tSampList_markers()" + COLOREND)

        tSampList : List[int] = []
        allEvents, allEvent_id = MneTestMaik.get_allEvents(rawBV)
        for i in range( len(allEvents) ):
            if( allEvents[i][2] == identifier ):
                tSampList.append( allEvents[i][0] )
        return tSampList

    @staticmethod
    def get_tSampDict_allMarkers(rawBV) -> dict:
        typesOfMarkers : List[str] = ["zBus", "shiftLeft", "shiftMiddle", "shiftRight", "button"]
        tSampDict_allMarkers : dict = {}
        for marker in typesOfMarkers:
            tSampDict_allMarkers[marker] = MneTestMaik.get_tSampList_markers(marker, rawBV)
        return tSampDict_allMarkers
    

    @staticmethod
    def get_targetList():
        return ["left", "middle", "right", "both", "right","middle","both","both","middle","both","middle","right","left","left","both","right","middle","middle","left","left"]
            # values for first maik pilot
            # later: get from ParticipantConstants
    


    @staticmethod
    def get_invalidBlocks_asIndices() -> List[int]:
        return [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    



    @staticmethod
    def gen_blockDict(rawBV) -> dict:
        tSampDict_allMarkers = MneTestMaik.get_tSampDict_allMarkers(rawBV)
        blockDict : dict = {}

        for i in range( len(tSampDict_allMarkers["zBus"]) ):
                # iterate through all blocks that were played

            blockLength_samples : int = 40 * int(rawBV.info["sfreq"]) # 40 s * 500 1/s = 20000
            blockStart_tSamp : int = tSampDict_allMarkers["zBus"][i] 
            blockEnd_tSamp : int = blockStart_tSamp + blockLength_samples

            tSampList_shiftLeft_blockX : List = []
            for shiftLeft in ( tSampDict_allMarkers["shiftLeft"] ):
                if( blockStart_tSamp <= shiftLeft <= blockEnd_tSamp ):
                    tSampList_shiftLeft_blockX.append( shiftLeft)

            tSampList_shiftMiddle_blockX : List = []
            for shiftMiddle in ( tSampDict_allMarkers["shiftMiddle"] ):
                if( blockStart_tSamp <= shiftMiddle <= blockEnd_tSamp ):
                    tSampList_shiftMiddle_blockX.append( shiftMiddle)

            tSampList_shiftRight_blockX : List = []
            for shiftRight in ( tSampDict_allMarkers["shiftRight"] ):
                if( blockStart_tSamp <= shiftRight <= blockEnd_tSamp ):
                    tSampList_shiftRight_blockX.append( shiftRight)

            tSampList_button_blockX : List = []
            for button in ( tSampDict_allMarkers["button"] ):
                if( blockStart_tSamp <= button <= blockEnd_tSamp ):
                    tSampList_button_blockX.append( button)

            # CAVE: first 4 blocks are testblocks! 
            # -> blockNr for normal blocks is not as expected (blockNrNEW = blockNrOLD + 4)
            # keep nrs as the are now for easier data processing later
            blockDict[f"block{i}"] = {
                    "zBus" : blockStart_tSamp, # only 1 entry
                    "shiftLeft": tSampList_shiftLeft_blockX,
                    "shiftMiddle": tSampList_shiftMiddle_blockX,
                    "shiftRight": tSampList_shiftRight_blockX,
                    "button" : tSampList_button_blockX
                }
        return blockDict

rawBV = MneTestMaik.get_prepared_rawBV()
tSampDict_allMarkers = MneTestMaik.get_tSampDict_allMarkers(rawBV)
print(rawBV.info["sfreq"])

blockDict = MneTestMaik.gen_blockDict(rawBV)
print(blockDict)

invalidBlockList = MneTestMaik.get_invalidBlocks_asIndices()
targetList = MneTestMaik.get_targetList()

correctPresses : int = 0
for b in range( len(tSampDict_allMarkers["zBus"])-1 ):
    if not( b in invalidBlockList):

        if( targetList[b] == "both"):
                # concatenate tSamp of left and right shifts
            tSamp_shiftsTargetStream = blockDict[f"block{b}"][f"shiftLeft"]
            for i in range( len(blockDict[f"block{b}"][f"shiftRight"]) ):
                tSamp_shiftsTargetStream.append( blockDict[f"block{b}"][f"shiftRight"][i] )
            tSamp_shiftsTargetStream.sort(reverse = False) # sort ints in ascending order
        else:  
            tSamp_shiftsTargetStream = blockDict[f"block{b}"][f"shift{targetList[b].capitalize()}"]
        
        tSamp_buttons = blockDict[f"block{b}"][f"button"]

        for shift in tSamp_shiftsTargetStream:
            if( any(shift <= button <= (shift + (rawBV.info["sfreq"]*1.5)) for button in tSamp_buttons) ):
                correctPresses += 1
total = len( tSamp_shiftsTargetStream ) # nr of presses expected for 100% correct
print(float(correctPresses)/float(total))
    # this should be equivalent to the rate needed for the pre-experiment later
    # but for the main experiment the score should be different,
    # including wrong presses somehow (in case the score shall be investigated at all)

# check whether score has been correctly calculated
# just for fun: test how many times wrongly pressed

