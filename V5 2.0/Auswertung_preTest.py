from typing import List


class Auswertung_preTest:

    def run_auswertung_preTest():

        #===============================================# 
        fileName = "preTest_participant0.vmrk"          #
        #===============================================# 

        filePath = "preTest_files" / fileName


        lines = Auswertung_preTest.readLines(filePath)
        lines_withoutTitle = Auswertung_preTest.removeTitle(lines)
        allMarkerOccurrences = Auswertung_preTest.get_allOccurrencesOfMarkers(lines_withoutTitle)
        print(allMarkerOccurrences)



    @staticmethod #from V6
    def readLines(filePath : str):
        """ Reads file and returns each line as a separate list entry """
        with open(filePath, "r") as f:
            lines : List[str]= f.readlines()
        return lines

    @staticmethod #from V6
    def removeTitle(lines : List[str]) -> List:
        """ Removes the first unnecessary lines from the .vmrk file """
        lines_withoutTitle : List[str] = []
        for i in range(11, len(lines)-1):
            lines_withoutTitle.append(lines[i])
        return lines_withoutTitle
    
    @staticmethod #from V6
    def get_allOccurrencesOfMarkers(lines_withoutTitle : List[str]) -> List[List]:
        """ Grabs marker occurrences as [markerName, markerTime] for all blocks """
        allMarkerOccurrences : List[List] = [] #List[List[str,int]]
        for l in lines_withoutTitle:
            markerName = l.split(sep = ",")[1]
            markerName = Auswertung_preTest.replaceMarkerNames(markerName)
            markerTime = int( l.split(sep = ",")[2] )
            allMarkerOccurrences.append( [markerName, markerTime])
        return allMarkerOccurrences
    
    @staticmethod #from V6
    def replaceMarkerNames(markerName):
        """ Help method for get_allOccurrencesOfMarkers(). """
        markerDict = {
            ""     : "startRecording",
            "S 97" : "?",
            "S 32" : "shiftLeft", 
            "S  2" : "shiftMiddle",
            "S  1" : "shiftRight",
            "S 65" : "zBus",
            "S128" : "button"
        }
        return markerDict[f"{markerName}"]