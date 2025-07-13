import freefield
from typing import List
import numpy as np
import time

import os
from pathlib import Path
import json

from Globals import Globals
from Paths import Paths
from Sequences import Sequences
from Sprecher_und_Procs import Sprecher_und_Procs
from ParticipantConstants import ParticipantConstants
from Generator import Generator



class Init_mainExp:

    @staticmethod
    def run_mainExp():

        #===============================================#               
                                                        #                            
        participantNr = 0                               #               
        #Mk:   0                                        #
        #Gl:   1                                        #
        #Tm:   2                                        #
        #Alx:  3                                        #
        #Blnc: 4                                        # 
                                                        #
        ampRise = 0.3                                   #
                                                        #             
        #===============================================#

        
        famsLMR = ParticipantConstants.get_famList(participantNr)
        blockDict : dict = {}

        ####

        while True:
            inp = input(Globals.COLORRED + "Remember to start recording! " + Globals.COLORCYAN + "Start? [yes]: " + Globals.COLOREND)
            if( inp.lower() == "yes"):
                break


        Sprecher_und_Procs.initFF()
        speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

        print(Globals.COLORCYAN + "Remember to comment the experiment in your Lab book." + Globals.COLOREND)

        ####_____________________________________________________________________

        for i in range(Globals.N_BLOCKS):

            target =  ParticipantConstants.get_targetList(participantNr)[i]
            Sprecher_und_Procs.turnTargetLedOn(leds, target)

            [nrSeqList_left, nrSeqList_middle, nrSeqList_right] = Generator.generate_nrSeqs_mainExp(ampRise)

            Sprecher_und_Procs.writeToSpeaker( "left",   speakers, famsLMR, nrSeqList_left )
            Sprecher_und_Procs.writeToSpeaker( "middle", speakers, famsLMR, nrSeqList_middle )
            Sprecher_und_Procs.writeToSpeaker( "right",  speakers, famsLMR, nrSeqList_right )
            print( f"nrSeqList_left = {nrSeqList_left}" )
            print( f"nrSeqList_middle = {nrSeqList_middle}" )
            print( f"nrSeqList_right = {nrSeqList_right}" )

            freefield.play()

            ##_____________________________________________________________________

            blockDict[f"block{i}"] = {}
            blockDict[f"block{i}"]["target"] = target
            blockDict[f"block{i}"]["nrSeqList_left"] = nrSeqList_left
            blockDict[f"block{i}"]["nrSeqList_middle"] = nrSeqList_middle
            blockDict[f"block{i}"]["nrSeqList_right"] = nrSeqList_right

            cwd = os.getcwd()
            cwd_mod = cwd.replace("V5 2.0", "Data Analysis 2.0\\blockDicts")
            pathFile : Path = f"{cwd_mod}\\participant{participantNr}\\participant{participantNr}_blockDict.txt" 
            with open(pathFile, "w") as f:
                json.dump(blockDict, f, indent = 4)

            ##_____________________________________________________________________

            time.sleep(len(nrSeqList_left))
            Sprecher_und_Procs.turnAllLedsOff(leds)

            inp = input("Continue with next block? [yes]: ")
            while True:
                if( inp.lower() == "yes" ):
                    break

        ####_____________________________________________________________________

        freefield.halt()
        print(Globals.COLORCYAN + "Remember to ask participant about their perception of the task." + Globals.COLOREND)

## 


#Init_mainExp.run_mainExp()


    