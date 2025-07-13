import os
from pathlib import Path
from typing import List
import re
import json



class ButtonPressAnalysis:
    # Klasse Fertig. Funktionalität getestet.
    # Achtung: Bei Änderung der Marker-Nummern können Inkompatibilitäten auftreten.
    # Achtung: Alle Nicht-Button-Marker scheinen mit ca. 1-1.5 Sekunden Verzögerung in BVR zu erscheinen.
    #          Die Zeitintervalle zwischen den Nicht-Button-Markern (z.B. Δt zwischen Shifts, und Δt zBus zu Shift) sind aber beinahe akkurat.

    participantNr               : int
    preTest_trial               : int

    pathVmrk                    : Path
    pathAmpRise_perSec          : Path

    samplerate                  : int               # 1 Sekunde = 500 Samples

    ampRiseTypes                : List[float]       # z.B. [0.15, 0.2] 
    ampRise_perSec              : List[float]       # z.B. [0.2, 0.0, 0.0, 0.15, 0.2, 0.0]
    ampRise_perShiftOcc         : List[float]       # z.B. [0.2, 0.15, 0.2]

    tSecRel_perMarker           : dict              # { 'S97' : [0.0], 'S 32' : [1.0, 7.0, ...], 'S128' : [1.622, 7.83, ...] }
    resultDict                  : dict


    @classmethod
    def __init__(cls):

        ###############################
        participantNr           = 0   #
        preTest_trial           = 0   #
        ###############################

        cls.pathVmrk            = Path( "button press files\\participant%d\\participant%d_preTest%d.vmrk"  %(participantNr, participantNr, preTest_trial) )
        cls.pathAmpRise_perSec  = Path( "button press files\\participant%d\\participant%d_preTest%d.txt"   %(participantNr, participantNr, preTest_trial) )
        cls.samplerate          = 500

        cls.ampRise_perSec      = ButtonPressAnalysis.get_ampRise_perSec_fromTxtFile( cls.pathAmpRise_perSec )
        cls.ampRise_perShiftOcc = ButtonPressAnalysis.entferneNullen( cls.ampRise_perSec )
        cls.ampRiseTypes        = ButtonPressAnalysis.extract_uniqueItems( cls.ampRise_perShiftOcc )

        cls.tSecRel_perMarker   = ButtonPressAnalysis.get_tSecRel_perMarker( cls.pathVmrk, cls.samplerate )

        cls.resultDict          = ButtonPressAnalysis.getResultDict( cls.ampRiseTypes, cls.tSecRel_perMarker, cls.ampRise_perShiftOcc )




    @staticmethod
    def get_ampRise_perSec_fromTxtFile(pathFile) -> List[float]:
        """ Liest jenes File, das die Liste enthält, welche den verwendeten ampRiseWert pro Sekunde angibt (d.h. nrSeqLeft)."""
        with open(pathFile, "r") as f:
            ampRise_perSec : List[float] = json.load(f)
        return ampRise_perSec

    @staticmethod
    def entferneNullen(liste : List[float]) -> List[float]:
        """ Entfernt Einträge, die shift-lose Sekunden repräsentieren. """
        neueListe : List[float] = []
        for e in liste:
            if( e != 0.0 ):
                neueListe.append(e)
        return neueListe
    
    @staticmethod
    def extract_uniqueItems(liste : List[float]) -> List[float]:
        """ Extrahiert alle in der Input-Liste vorhandenen Eintrags-Typen.
            Die Output-Liste repräsentiert die Menge an Einträgen der Input-Liste. """
        uniqueItems : List[float] = []
        for zahl in liste:
            if zahl not in uniqueItems:
                uniqueItems.append(zahl)
        uniqueItems.sort()
        return uniqueItems



    @staticmethod
    def leseAusDatei(pathFile : Path) -> List[str]:
        with open(pathFile, "r") as f:
            lines : List[str] = f.readlines()
            return lines
        
    @staticmethod
    def entferneIrrelevanteZeilen(lines : List[str]) -> List[str]:
        """ Entfernt die einleitenden Zeilen des VMRK Files, die für die Datenanalyse nicht benötigt werden. """
        for i in range(0,12):
            lines.pop(0)
        return lines

    @staticmethod
    def extrahiereMarkerZeiten_sampAbs(pathFile : Path) -> dict:
        """ Hilfs-Funktion für removeBouncing(). """
        lines = ButtonPressAnalysis.leseAusDatei(pathFile)
        lines = ButtonPressAnalysis.entferneIrrelevanteZeilen(lines)

        zBusList = []
        shiftLeftList = []
        buttonList = []

        tSampAbs_perMarker : dict = {
            "S161" : zBusList, #zBus
            "S 32" : shiftLeftList, #shiftLeft
            "S128" : buttonList  #button
        }
        for line in lines:
            marker  = re.findall( r"S\s{0,3}\d{1,3}", line )[0]
            absTime = re.findall( r"\d+", line )[2]
            tSampAbs_perMarker[f"{marker}"].append( int(absTime) )
        return tSampAbs_perMarker

    @staticmethod
    def konvertiereZu_SampRel(tSampAbs_perMarker : dict) -> dict:
        """ Hilfs-Funktion für removeBouncing(). """
        t_zBus = tSampAbs_perMarker["S161"][0]
        
        zBusList = []
        shiftLeftList = []
        buttonList = []

        tSampRel_perMarker : dict = {
            "S161" : zBusList, #zBus
            "S 32" : shiftLeftList, #shiftLeft
            "S128" : buttonList  #button
        }
        for key in tSampAbs_perMarker:
            for listEntry in tSampAbs_perMarker[key]:
                tSampRel_perMarker[key].append( listEntry - t_zBus )
        return tSampRel_perMarker
                
    @staticmethod
    def konvertiereZu_SecRel(samplerate : int, tSampRel_perMarker : dict) -> dict:
        """ Hilfs-Funktion für removeBouncing(). """
        zBusList = []
        shiftLeftList = []
        buttonList = []

        tSecRel_perMarker : dict = {
            "S161" : zBusList,      #zBus
            "S 32" : shiftLeftList, #shiftLeft
            "S128" : buttonList     #button
        }

        for key in tSampRel_perMarker:
            for listEntry in tSampRel_perMarker[key]:
                tSecRel_perMarker[key].append( listEntry / samplerate )
        return tSecRel_perMarker

    @staticmethod
    def get_tSecRel_perMarker( pathVmrk : Path, samplerate : int ) -> dict:
        """ Liest die Zeitpunkte von Marker-Ereignissen aus dem VMRK File.
            Berücksichtigt werden Marker für den zBus (S 97), shiftLeft (S 32) und button (S128).
            Danach werden alle Zeitpunkte wie folgt formatiert:
                Das Auftreten des zBusses wird als t = 0 definiert.
                Die Zeitpunkte werden von der Anzahl an Samples in die Anzahl an Sekunden konvertiert. """
        
        tSampAbs_perMarker : dict = ButtonPressAnalysis.extrahiereMarkerZeiten_sampAbs( pathVmrk )
        tSampRel_perMarker : dict = ButtonPressAnalysis.konvertiereZu_SampRel( tSampAbs_perMarker )
        tSecRel_perMarker  : dict = ButtonPressAnalysis.konvertiereZu_SecRel(  samplerate, tSampRel_perMarker )
        tSecRel_perMarker["S128"] = ButtonPressAnalysis.removeBouncing( tSecRel_perMarker["S128"] ) #überschreibt alte Liste
        return tSecRel_perMarker
    
    @staticmethod
    def removeBouncing(buttonList : List[float]) -> List[float]:
        """ Entfernt Zeitpunkte von Knopfdruck-Markern, wenn diese offensichtlicherweise durch einen Wackelkontakt ausgelöst wurden.
            Wenn ein Knopfdruck-Marker innerhalb von 0.25 Sekunden nach einem anderen Knopfdruck-Marker auftritt, so wird dieser entfernt. """
        
        advancedButtonList1 : List[float] = buttonList.copy()

        for i in range( len(buttonList)-1, -1, -1): # for( i=len-1 ; i=>0 ; i-- )
            # Bouncing: Zweiter Marker tritt meistens weiger als 0.2 Sekunden nach erstem Marker auf
            if( buttonList[i] - 0.25 <= buttonList[i-1] <= buttonList[i] ): 
                advancedButtonList1[i] = -6.6 # Nur ein Platzhalter
        
        advancedButtonList2 = [value for value in advancedButtonList1 if value != -6.6] # Übernimmt alle Werte der alten Liste, die nicht -6.6 sind
        return advancedButtonList2



    @staticmethod
    def getResultDict( ampRiseTypes : List[float], tSecRel_perMarker : dict, ampRise_perShiftOcc : List[float] ) -> dict:
        """ Zählt die Anzahl an Ereignissen, bei denen ein Knopf nach Auftreten eines Shifts gedrückt wurde. 
            Die Zählung erfolgt separat für jeden Lautstärke-Erhöhungs-Wert. 
            Es werden Knopfdrücke im Bereich von -0.5 Sekunden vor bis 1.5 Sekunden nach Auftreten des Shift-Markers berücksichtigt,
            da die Knopfdruck-Marker im Bezug auf die Shift-Marker zeitlich vor-verschoben scheinen."""
        
        resultDict = {}
        for ampRiseType in ampRiseTypes:
            resultDict[f"{ampRiseType}"] = 0 # Counter wird auf Default-Wert (= 0) gesetzt
        
        for i in range( len( tSecRel_perMarker["S 32"] ) ): # Heraussuchen aller Shift-Ereignisse
            t_shift = tSecRel_perMarker["S 32"][i]          #

            for t_button in tSecRel_perMarker["S128"]:             # Vergleich der Zeitpunkte der Button-Ereignisse mit den Shift-Ereignissen
                if( t_shift - 0.5 <= t_button <= t_shift + 1.5):   # ! Die Button-Marker scheinen häufig kurz vor dem Shift-Marker aufzutreten
                    ampRiseType = ampRise_perShiftOcc[i]           # Zum Shift-Ereignis zugehöriger ampRise-Typ wird herausgesucht
                    resultDict[f"{ampRiseType}"] += 1              # Counter des zugehörigen AmpRise-Types wird um 1 erhöht
        return resultDict



#ButtonPressAnalysis()
#print(ButtonPressAnalysis.resultDict)
