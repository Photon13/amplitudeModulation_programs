from typing import List
import random
import numpy as np

from Globals import Globals


class Generator:

    @staticmethod
    def generate_nrSeqs_mainExp(ampRise : float) -> List:
        """ returns [nrSeqLeft, nrSeqMiddle, nrSeqRight] 
            Gesamt 30 Sekunden per Block, mit den ersten drei Sekunden ohne Shift """
    
        dreiSechsList = []
        dreiSechsList.extend( [3] * 3 )  # 9 sec
        dreiSechsList.extend( [6] * 3 )  # 18 sec
        random.shuffle(dreiSechsList)

        listOfLists = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]] # 3 sec
        for i in range( len(dreiSechsList) ):
            random.shuffle(listOfLists)
            listOfLists[0].append( ampRise )
            listOfLists[0].extend( Generator.generateListOfZeros( dreiSechsList[i] - 1) )
            listOfLists[1].extend( Generator.generateListOfZeros( dreiSechsList[i])     )
            listOfLists[2].extend( Generator.generateListOfZeros( dreiSechsList[i])     )

        random.shuffle(listOfLists)
        return listOfLists #[nrSeqLeft, nrSeqMiddle, nrSeqRight]



    @staticmethod
    def generate_nrSeq_preTest(ampRiseRange : List[float]) -> List:
        """ returns 2 listWithShifts: first half and second half
            [listWithShifts1, listWithShifts2]
            Gesamt 3 + 336 Sekunden mit den ersten drei Sekunden ohne Shift.
            Jede Hälfte ca. 2-3 Minuten lang. """

        dreiSechsList = []
        dreiSechsList.extend( [3] * int(80*0.6) ) #48*3sec
        dreiSechsList.extend( [6] * int(80*0.4) ) #32*6sec
        
        random.shuffle(dreiSechsList)

        ampRiseList = Generator.generate_valuesInRange( ampRiseRange, n_values = 8  )
        ampRiseList = Generator.duplicateListEntries(   ampRiseList,  n = 10        )
        random.shuffle(ampRiseList)

        n = len(ampRiseList)
        half = int(n/2)

        listFirstHalf : List[float] = [0.0, 0.0, 0.0]
        for i in range( 0, half ):
            listFirstHalf.append(ampRiseList[i])
            n_zeros = dreiSechsList[i] -1
            listFirstHalf.extend(Generator.generateListOfZeros(n_zeros))

        listSecondHalf : List[float] = [0.0, 0.0, 0.0]
        for i in range( half, n ):
            listSecondHalf.append(ampRiseList[i])
            n_zeros = dreiSechsList[i] -1
            listSecondHalf.extend(Generator.generateListOfZeros(n_zeros))

        return [listFirstHalf, listSecondHalf]
    

    @staticmethod
    def generateListOfZeros(length : int) -> List[float]:
        result = []
        result.extend([0.0]*length)
        return result

    #---------------------------------------------------------------------------------

    @staticmethod
    def duplicateListEntries(list : List, n : int) -> List: #works
        """ result contains each value of original list n-times"""
        result : List = []
        for entry in list:
            result.extend( [entry]*n )
        return result

    

    @staticmethod #works
    def generate_valuesInRange(borders : List[float], n_values : int):
        result : List[float] = []
        result.append( min(borders) )            # first entry is lower border
        difference = max(borders)-min(borders)
        step = difference/(n_values-1)           # using log values does not seem to make a difference ... spaces stay the same
        for i in range( n_values-1 ):            # -1 because first entry already in list
            entry = result[-1] + step            # List[-1] returns last value
            result.append( round(entry,3) )
        return result # all values equally spaced
    
    #---------------------------------------------------------------------------------
    
    @staticmethod
    def generate_targetList():
        targetList : List[str] = []
        possTargets = ["left", "middle", "right", "both"]
        for target in possTargets:
            targetList.extend([target]*4)
        random.shuffle(targetList)
        return targetList