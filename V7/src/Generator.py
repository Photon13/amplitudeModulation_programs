from typing import List
import random

class Generator:

    @staticmethod
    def generate_targetList():
        targetList : List[str] = []
        possTargets = ["left", "middle", "right", "both"]
        for target in possTargets:
            targetList.extend([target]*4)
        random.shuffle(targetList)
        return targetList



    @staticmethod
    def generate_nrSeqs_mainExp(ampRise):
        """ returns [nrSeqLeft, nrSeqMiddle, nrSeqRight] """
        listOfLists = [ [], [], [] ]

        nList = []
        nList.extend( [3] * (30*0.6) ) #18*3sec = 54sec
        nList.extend( [6] * (30*0.4) ) #12*6sec = 72 sec
        #total 90sec
        random.shuffle(nList)

        for n in nList:
            random.shuffle(listOfLists)
            listOfLists[0].extend(ampRise)
            listOfLists[0].extend(Generator.generateListOfZeros(n-1))
            listOfLists[1].extend(Generator.generateListOfZeros(n))
            listOfLists[2].extend(Generator.generateListOfZeros(n))

        random.shuffle(listOfLists)
        return listOfLists #[nrSeqLeft, nrSeqMiddle, nrSeqRight]


    @staticmethod
    def generate_nrSeqs_preTest(ampRiseRange : List[float]):
        listWithShifts = []
        
        nList = []
        nList.extend( [3] * (80*0.6) ) #48*3sec
        nList.extend( [6] * (80*0.4) ) #32*6sec
        #total 336sec
        random.shuffle(nList)

        ampRiseList = Generator.generate_valuesInRange( ampRiseRange, n_values=8 )
        ampRiseList = Generator.duplicateListEntries( ampRiseList, n=10 )
        random.shuffle(ampRiseList)

        for n in nList:
            listWithShifts.extend(ampRiseList[n])
            listWithShifts.extend(Generator.generateListOfZeros(n-1))

        listWithZeros = Generator.generateListOfZeros( len(listWithShifts) )
        return [listWithShifts, listWithZeros, listWithZeros]



    @staticmethod
    def generateListOfZeros(length : int) -> List[float]:
        result = []
        result.extend([0.0]*length)
        return result

    @staticmethod
    def duplicateListEntries(list : List, n : int) -> List: #works
        """ result contains each value of original list n-times"""
        result : List = []
        for entry in list:
            result.extend( [entry]*n )
        return result



    @staticmethod
    def generate_valuesInRange(borders : List[float], n_values : int):
        result : List[float]
        result.append( min(borders) )            # first entry is lower border
        difference = max(borders)-min(borders)
        step = difference/(n_values-1)           # using log values does not seem to make a difference ... spaces stay the same
        for i in range( n_values-1 ):             # -1 because first entry already in list
            entry = result[-1] + step            # List[-1] returns last value
            result.append( round(entry,3) )
        return result
    



#print(duplicateListEntries(["huhu"], 3))

