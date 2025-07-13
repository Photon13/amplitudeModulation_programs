from typing import List
import random
import numpy as np

from Globals import Globals
from ParticipantConstants import ParticipantConstants

class Generator:

    @staticmethod
    def gen_pre_AmpRiseList(possRiseValues : List[float]):
        riseList : List[float] = []
        for riseValue in possRiseValues:
            for i in range(10):
                riseList.append(riseValue)
        
        random.shuffle(riseList) # returns None

        nullPoss : List[List[float]] = [ [0.0], [0.0, 0.0], [0.0, 0.0, 0.0] ]
        nullList : List[List[float]] = random.choices(population = nullPoss, weights = [0.5, 0.3, 0.2], k = len(riseList))

        ampRise : List[float] = [0.0, 0.0, 0.0]
        for i in range( len(riseList) ):
            ampRise.append(riseList[i])
            for j in range( len(nullList[i]) ):
                ampRise.append(nullList[i][j])
        return ampRise
    
    @staticmethod
    def gen_empty_AmpRiseList(length : int):
        emptyList = []
        for i in range(length):
            emptyList.append(0.0)
        return emptyList




    @staticmethod
    def gen_ampRiseArray(possRiseValues : List[float], preExperiment : bool):
        ampRiseList = Generator.gen_AmpRiseList(possRiseValues, preExperiment) 
        return np.array(ampRiseList).astype('float64')

    @staticmethod
    def gen_ampRiseArray_mainExperment():
        participantNr = ParticipantConstants.currentParticipantNr
        ampRise = ParticipantConstants.AMP_RISE_01234[participantNr]
        ampRiseList = Generator.gen_ampRiseArray([ampRise], preExperiment = False )

        return np.array(ampRiseList).astype('float64')





    @staticmethod
    def gen_shiftOccurrence_withoutShifts() -> List[str]:
        shiftOccurrence : List[str] = ["none"]
        for i in range(1, Globals.N_SUBBLOCKS):
            shiftOccurrence.append("none")
        return shiftOccurrence
    
    @staticmethod
    def gen_shiftOccurrence_soloSpeaker(shiftPosition : str) -> List[str]:
        shiftOccurrence : List[str] = ["none"]
        for i in range(1, Globals.N_SUBBLOCKS):
            shiftOccurrence.append(shiftPosition)
        return shiftOccurrence
    
    @staticmethod
    def gen_shiftOccurrence() -> List[str]:
        shiftOccurrence : List[str] = ["none"]
        for i in range(1, Globals.N_SUBBLOCKS):
            shiftOccurrence.append(random.choice(["left", "middle", "right"]))
        return shiftOccurrence
    
    @staticmethod
    def generate_blockShiftDict():
        blockShiftDict : dict = {}
        for i in range(Globals.N_BLOCKS):
            blockShiftDict[f"block{i}"] = Generator.gen_shiftOccurrence()
        return blockShiftDict
    
    
    @staticmethod
    def generate_random_targetList() -> List[str]: 
        x : List[str] = ["left", "middle","right"] 
        random.shuffle(x)

        targetList : List[str] = []
        targetList.append(x[0])
        targetList.append(x[1])
        targetList.append(x[2])
        targetList.append("both")
        y : List[str] = []
                             
        y.extend( 4*["left"])
        y.extend( 4*["right"])
        y.extend( 4*["middle"])
        y.extend( 4*["both"])
        random.shuffle(y)

        for target in y:
            targetList.append(target)
        return targetList

#print(Generator.gen_ampRiseList_preExperiment([0.1, 0.2, 0.3]) )

#print(Generator.generate_blockShiftDict())

#for i in range(5):
#    print(Generator.generate_random_targetList())


