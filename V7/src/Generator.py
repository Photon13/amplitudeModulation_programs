from typing import List
import random


class Generator:

    @staticmethod #works
    def generate_targetList():
        targetList : List[str] = []
        possTargets = ["left", "middle", "right", "both"]
        for target in possTargets:
            targetList.extend([target]*4)
        random.shuffle(targetList)
        return targetList

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @staticmethod #works
    def generate_nrSeqs_mainExp(ampRise : float) -> List:
        """ returns [nrSeqLeft, nrSeqMiddle, nrSeqRight] """
        listOfLists = [[], [], []]

        nList = []
        nList.extend( [3] * int(30*0.6) ) #18*3sec = 54sec
        nList.extend( [6] * int(30*0.4) ) #12*6sec = 72 sec
        #total 90sec # total length = 126 ?????????
        random.shuffle(nList)

        for n in nList:
            random.shuffle(listOfLists)
            listOfLists[0].append(ampRise)
            listOfLists[0].extend(Generator.generateListOfZeros(n-1))
            listOfLists[1].extend(Generator.generateListOfZeros(n))
            listOfLists[2].extend(Generator.generateListOfZeros(n))

        random.shuffle(listOfLists)
        return listOfLists #[nrSeqLeft, nrSeqMiddle, nrSeqRight]


    @staticmethod #works
    def generate_nrSeqs_preTest(ampRiseRange : List[float]) -> List:
        listWithShifts = []
        
        nList = []
        nList.extend( [3] * int(80*0.6) ) #48*3sec
        nList.extend( [6] * int(80*0.4) ) #32*6sec
        #total 336sec #sic
        random.shuffle(nList)

        ampRiseList = Generator.generate_valuesInRange( ampRiseRange, n_values=8 )
        ampRiseList = Generator.duplicateListEntries( ampRiseList, n=10 )
        random.shuffle(ampRiseList)

        for n in nList:
            listWithShifts.append(ampRiseList[n])
            listWithShifts.extend(Generator.generateListOfZeros(n-1))

        listWithZeros = Generator.generateListOfZeros( len(listWithShifts) )
        return [listWithShifts, listWithZeros]

    #---------------------------------------------------------------------------------
    
    @staticmethod #works
    def generateListOfZeros(length : int) -> List[float]:
        result = []
        result.extend([0.0]*length)
        return result

    #---------------------------------------------------------------------------------

    @staticmethod #works
    def duplicateListEntries(list : List, n : int) -> List: #works
        """ result contains each value of original list n-times"""
        result : List = []
        for entry in list:
            result.extend( [entry]*n )
        return result

    #---------------------------------------------------------------------------------

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
    



#listOfLists = Generator.generate_nrSeqs_mainExp(0.3)
#for i in range(0,8):
#    print (listOfLists[0][i], end = " ")
#print("\n")
#for j in range(0,8):
#    print (listOfLists[1][j], end = " ")
#print("\n")
#for k in range(0,8):
#    print (listOfLists[2][k], end = " ")

#print(len(listOfLists[1]))
#print(len(listOfLists[1]))
#print(len(listOfLists[2]))

