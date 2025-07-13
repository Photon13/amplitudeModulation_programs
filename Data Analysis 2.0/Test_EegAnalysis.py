import mne
import os
from pathlib import Path
import re
import json


def lade_blockDict(pathFile):
    with open(pathFile, "r") as f:
        blockdict = json.load(f)
    return blockdict

def get_blocksPerTarget(blockDict):
    blocksLeft   = []
    blocksMiddle = []
    blocksRight  = []
    blocksBoth   = []

    for block in blockDict:
        if( blockDict[block]["target"] == "left" ):
            blocksLeft.append(block)
        elif( blockDict[block]["target"] == "middle" ):
            blocksMiddle.append(block)
        elif( blockDict[block]["target"] == "right" ):
            blocksRight.append(block)
        elif( blockDict[block]["target"] == "both" ):
            blocksBoth.append(block)
        
    blocksPerTarget : dict = {
        "left" : blocksLeft,
        "middle" : blocksMiddle,
        "right" : blocksRight,
        "both" : blocksBoth
    }
    return blocksPerTarget



participantNr = 0
pathFile = Path(f"blockDicts\\participant{participantNr}_blockDict.txt")
blockDict = lade_blockDict(pathFile)
blocksPerTarget = get_blocksPerTarget(blockDict)
print(blocksPerTarget)