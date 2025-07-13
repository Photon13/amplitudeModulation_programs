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
        # length list correct
        # no simultaneous shifts
        """ returns [nrSeqLeft, nrSeqMiddle, nrSeqRight] """
    
        dreiSechsList = []
        dreiSechsList.extend( [3] * 16 ) # 2/3
        dreiSechsList.extend( [6] * 8  ) # 1/3
        #total 96sec per block
        random.shuffle(dreiSechsList)

        listOfLists = [[], [], []]
        for i in range( len(dreiSechsList) ):
            random.shuffle(listOfLists)
            listOfLists[0].append( ampRise )
            listOfLists[0].extend( Generator.generateListOfZeros( dreiSechsList[i] - 1) )
            listOfLists[1].extend( Generator.generateListOfZeros( dreiSechsList[i]) )
            listOfLists[2].extend( Generator.generateListOfZeros( dreiSechsList[i]) )

        random.shuffle(listOfLists)
        return listOfLists #[nrSeqLeft, nrSeqMiddle, nrSeqRight]


    @staticmethod #works
    def generate_nrSeq_preTest(ampRiseRange : List[float]) -> List:
        # length list correct
        # n occurrences per value correct

        dreiSechsList = []
        dreiSechsList.extend( [3] * int(80*0.6) ) #48*3sec
        dreiSechsList.extend( [6] * int(80*0.4) ) #32*6sec
        #total 336sec #sic
        random.shuffle(dreiSechsList)

        ampRiseList = Generator.generate_valuesInRange( ampRiseRange, n_values=8 )
        ampRiseList = Generator.duplicateListEntries( ampRiseList, n=10 )
        random.shuffle(ampRiseList)

        listWithShifts = []
        for i in range( len(ampRiseList) ):
            listWithShifts.append(ampRiseList[i])
            n_zeros = dreiSechsList[i] -1
            listWithShifts.extend(Generator.generateListOfZeros(n_zeros))

        return listWithShifts

    #---------------------------------------------------------------------------------
    
    @staticmethod 
    def generate_nrSeq_withShifts(length : int, ampRiseValue : int) -> List[float]:
        # example output: [0.0, 0.0, 0.0, 7.0, 0.0, 0.0, 7.0, 0.0, 0.0, 7.0, 0.0, 0.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 0.0]
        nrSeq = Generator.generateListOfZeros( length )
        i = 0
        while True:
            choice = random.choices( [3, 6], [0.6, 0.4], k=1 )[0]
            i += choice
            if( i >= length-1 ):
                break
            nrSeq[i] = ampRiseValue     
        return nrSeq

    
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

