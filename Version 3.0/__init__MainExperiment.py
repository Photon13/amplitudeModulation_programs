from BlockDict import BlockDict
from LoopParams import FreqComb, Conditions, Trials
from ProcsSprecherLeds import Procs, Sprecher, Leds
from Generator import Generator

import time
import json
from typing import List

import freefield

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORGREEN  = "\033[0;32m"
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


class MainExperiment:

    @staticmethod
    def run_mainExperiment():

        #####################
        pNr = 3             #          # <---
                            #                                   # Mk:0,    Gl:1,   Tm:2,   Alx:3,   Blnc:4
        ampRise = 0.286       #          # <---
        #####################

        pathBlockDict =  BlockDict.get_pathBlockDict( pNr ) 
        pathNrSeqs    =  BlockDict.get_pathNrSeqs( pNr )

        while True:
            inp = input(COLORRED + "Remember to start recording! " + COLORCYAN + "Start? [yes]: " + COLOREND)
            if( inp.lower() == "yes"):
                break

        Procs.initFF()
        speakers, leds = Procs.pickSpeakersAndLeds()
        blockDict = BlockDict.lade_blockDict( pathBlockDict )

        count = 0 
        for i in range( len(blockDict) ):
            

            target    : str         = blockDict[f"block{i}"]["condition"]
            freqComb  : str         = blockDict[f"block{i}"]["freqComb"]
            famsLMR   : List[float] = FreqComb.get_fams_fromFreqComb( freqComb )
            nrSeqsLMR : List[List]  = Generator.generate_nrSeqs_mainExp(ampRise)

            print(COLORPURPLE + f"block{i}   target = {target}\n" + COLOREND)

            with open( pathNrSeqs, "a" ) as f:
                f.write(   f"nrSeqLeft = {nrSeqsLMR[0]}\n"   ) # einfach nur reinmüllen
                f.write( f"nrSeqMiddle = {nrSeqsLMR[1]}\n"   )
                f.write(  f"nrSeqRight = {nrSeqsLMR[2]}\n\n" )

            Leds.turnTargetLedOn(leds, target)
            time.sleep(3)

            Sprecher.writeToSpeaker( "left",   speakers, famsLMR, nrSeqsLMR[0] )
            Sprecher.writeToSpeaker( "middle", speakers, famsLMR, nrSeqsLMR[1] )
            Sprecher.writeToSpeaker( "right",  speakers, famsLMR, nrSeqsLMR[2] )

            freefield.play()
            time.sleep( len( nrSeqsLMR[0]) )   
        
            count += 1 
            if( count == 4): # n blocks nach denen Pause auftreten soll
                while True:
                    inp = input("Continue? [yes]: ")
                    if( inp.lower() == "yes"):
                        break
                
                count = 0
            Leds.turnAllLedsOff(leds)
            time.sleep(3) # zeitlicher Puffer bevor nächste Daten geladen werden
                

        freefield.halt()  
        print(f"blockDict = {blockDict}")

##############################################################################################################################################

MainExperiment.run_mainExperiment()

#participant13 : 20 sec pause nach 4 blocks
# start: 180 sec pause, passt