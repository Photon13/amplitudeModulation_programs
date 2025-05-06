from Paths import Paths
from GeneratorPreTest import GeneratorPreTest
from Dateien_und_Json import Dateien_und_Json

import re
from pathlib import Path
from typing import List

COLORBLUE   = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORPURPLE = '\033[35m'
COLORYELLOW = '\033[33m'
COLORFAT = '\033[1m'
COLOREND = '\033[0m'

class AnalysisPreTest_withoutMne:

    @staticmethod
    def readLines(filePath : str):
        """ Reads file and returns each line as a separate list entry """
        with open(filePath, "r") as f:
            lines : List[str]= f.readlines()
        return lines

    @staticmethod
    def removeTitle(lines : List[str]) -> List:
        """ Removes the first unnecessary lines from the .vmrk file """
        lines_withoutTitle : List[str] = []
        for i in range(11, len(lines)-1):
            lines_withoutTitle.append(lines[i])
        print(lines_withoutTitle)
        return lines_withoutTitle
    
    @staticmethod
    def replaceMarkerNames(markerName):
        markerDict = {
            ""     : "StartRecording",
            "S 32" : "shiftLeft", 
            "S  2" : "shiftMiddle",
            "S  1" : "shiftRight",
            "S 65" : "zBus",
            "S128" : "button"
        }
        return markerDict[f"{markerName}"]
    
    @staticmethod
    def get_allOccurrencesOfMarkers(lines_withoutTitle : List[str]) -> List[List]:
        """ Grabs marker occurrences as [markerName, markerTime] for all blocks """
        allMarkerOccurrences : List[List] = [] #List[List[str,int]]
        for l in lines_withoutTitle:
            markerName = l.split(sep = ",")[1]
            markerName = AnalysisPreTest_withoutMne.replaceMarkerNames(markerName)
            markerTime = int( l.split(sep = ",")[2] )
            allMarkerOccurrences.append( [markerName, markerTime])
        return allMarkerOccurrences
    
    @staticmethod
    def get_allMarkerOccurrences_perBlock(allMarkerOccurrences : List[List]) -> dict:
        """ Assigns marker occurrences (=[markerName, markerTime]) to respective block """
        zBus_occurrences : List[int] = []
        shiftLeft_occurrences : List[int] = []
        shiftMiddle_occurrences : List[int] = []
        shiftRight_occurrences : List[int] = []
        button_occurrences : List[int] = []

        for entry in allMarkerOccurrences:
            if( entry[0] == "zBus"):
                zBus_occurrences.append( entry[1])
            elif( entry[0] == "shiftLeft"):
                shiftLeft_occurrences.append( entry[1])
            elif( entry[0] == "shiftMiddle"):
                shiftMiddle_occurrences.append( entry[1])
            elif( entry[0] == "shiftRight"):
                shiftRight_occurrences.append( entry[1])
            elif( entry[0] == "button"):
                button_occurrences.append( entry[1])

        blockDictMarkerOccurrences : dict = {}
        print(COLORBLUE + f"{zBus_occurrences}" + COLOREND)
        for i in range( len(zBus_occurrences) ):
            blockStart_samp = zBus_occurrences[i]
            blockLength_samp : int = blockLength * sfreq
            blockEnd_samp = blockStart_samp + blockLength_samp

            shiftLeft_occurrences_blockX : List[int] = []
            for shiftLeft in shiftLeft_occurrences:
                if( blockStart_samp <= shiftLeft <= blockEnd_samp ):
                    shiftLeft_occurrences_blockX.append( shiftLeft )

            shiftMiddle_occurrences_blockX : List[int] = []
            for shiftMiddle in shiftMiddle_occurrences:
                if( blockStart_samp <= shiftMiddle <= blockEnd_samp ):
                    shiftMiddle_occurrences_blockX.append( shiftMiddle )

            shiftRight_occurrences_blockX : List = []
            for shiftRight in shiftRight_occurrences:
                if( blockStart_samp <= shiftRight <= blockEnd_samp ):
                    shiftRight_occurrences_blockX.append( shiftRight )

            button_occurrences_blockX : List = []
            for button in button_occurrences:
                if( blockStart_samp <= button <= blockEnd_samp ):
                    button_occurrences_blockX.append( button )
            
            blockDictMarkerOccurrences[f"block{i}"] = {
                "zBus" : blockStart_samp,
                "shiftLeft": shiftLeft_occurrences_blockX,
                "shiftMiddle": shiftMiddle_occurrences_blockX,
                "shiftRight": shiftRight_occurrences_blockX,
                "button" : button_occurrences_blockX
            }
            return blockDictMarkerOccurrences

    @staticmethod 
    def get_possAmpRiseValues(blockDict : dict):
        """ Grabs all tested ampRise values from the nrSeqs """
        possAmpRiseValues : List[float] = []
        for i in range( blockDict["n_blocks"] ): # loop through blocks
            for j in range( len(blockDict[f"block{i}"]["nrSeqLeft"]) ):
                for pos in ["Left", "Middle", "Right"]:
                    entry = blockDict[f"block{i}"][f"nrSeq{pos}"][j] # search in all nrSeqs (just in case they were used)
                    if( entry != 0.0 ): # if entry is not 0.0
                        if( possAmpRiseValues.count(entry) == 0 ): # if value does not yet exist in list
                            possAmpRiseValues.append(entry)

        possAmpRiseValues.sort()
        return possAmpRiseValues
    
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#
sfreq = 500 #Hz
blockLength : int = 40 #sec

identifier : str = "testMarkerAnalysis0"

targets = ["left"] #always
#§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§#


fileBVName = f"{identifier}.vmrk"
fileJsonName = f"{identifier}_preTest.txt"

fileBVPath = Dateien_und_Json.get_pathBVFile(fileBVName)
lines : List[str] = AnalysisPreTest_withoutMne.readLines(fileBVPath)
lines_withoutTitle = AnalysisPreTest_withoutMne.removeTitle(lines)
allMarkerOccurrences = AnalysisPreTest_withoutMne.get_allOccurrencesOfMarkers(lines_withoutTitle)
blockDictMarkerOccurrences = AnalysisPreTest_withoutMne.get_allMarkerOccurrences_perBlock(allMarkerOccurrences)

print(blockDictMarkerOccurrences)

blockDict = Dateien_und_Json.readJson(fileJsonName)
possibleAmpRiseValues = AnalysisPreTest_withoutMne.get_possAmpRiseValues(blockDict)

resultDict : dict = {}
for val in possibleAmpRiseValues:
    n_correct = 0
    for target in targets:
        shifts = blockDictMarkerOccurrences[f"shift{target.capitalize()}"]
        buttons = blockDictMarkerOccurrences["button"]
        for s in shifts:
            lowerB : float = s + 0.1*sfreq   # intervall lower border  : 0.1 sec after shift
            higherB : float = s + 1.75*sfreq # intervall higher border : 1.75 sec after shift
            if( any( lowerB <= b <= higherB for b in buttons) ):
                n_correct += 1
    total : int = 10
    score : float = n_correct / float(total)
    resultDict[f"val"] = score

print(resultDict)