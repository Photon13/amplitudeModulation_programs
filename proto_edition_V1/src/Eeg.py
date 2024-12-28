from typing import List
import os
from pathlib import Path
import re

from Globals import Globals

class Eeg:



    def get_fileList(pathFolder : Path) -> List[str]:
        
        dirList : List[str] = os.listdir(pathFolder)
        fileList : List[str] = []

        for entry in dirList:
            if os.path.isfile(pathFolder / entry) == True:
                fileList.append(entry)
        return fileList
    



    def get_properFileList(searchPattern : str, pathFolder : Path):

        fileList : List[str] = Eeg.get_fileList(pathFolder)
        properFileList : List[str] = []
        
        for fileName in fileList:
        
            if( re.search(searchPattern, fileName) != None):
                properFileList.append(fileName)
        return properFileList

    @staticmethod
    def getAllEegFiles_forSingleParticipant(participantNr : int) -> dict:
        """ Help method for -> Participant.add_eegFileDict(self) -> Auswertung.wrapper_auswertungSingleParticipant()
                Grabs all  .eeg, .vdhr and .vmrk  for given participant nr 
                and returns them as  dict of List[str] """

        # participantNr is used by search pattern in Globals
        
        list_filesExtension_eeg : List[str] = Eeg.get_properFileList(Globals.SEARCH_PATTERN_eeg, Globals.PATH_FOLDER_EEG_RAW)
        print(f"{list_filesExtension_eeg}\n")
        
        list_filesExtension_vhdr : List[str] = Eeg.get_properFileList(Globals.SEARCH_PATTERN_vhdr, Globals.PATH_FOLDER_EEG_RAW)
        print(f"{list_filesExtension_vhdr}\n")
        
        list_filesExtension_vmrk : List[str] = Eeg.get_properFileList(Globals.SEARCH_PATTERN_vmrk, Globals.PATH_FOLDER_EEG_RAW)
        print(f"{list_filesExtension_vmrk}\n")
        
        eegFileDict = {
            "list_filesExtension_eeg" : list_filesExtension_eeg,
            "list_filesExtension_vhdr" : list_filesExtension_vhdr,
            "list_filesExtension_vmrk" : list_filesExtension_vmrk
        }
        return eegFileDict


    def testVrvrakk_searchRawFiles() -> None:
        pathFolder_testEeg : Path = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG\\test_eeg_files")
        pathFolder_testEegRaw : Path = pathFolder_testEeg / "raw_vrvrakk"
        ##
        searchPattern = re.compile(r""" ^(ad_)                  # start str
                                        [ae]                    # a or e  
                                        ( (\d) | (\d_\d) )      # some digit or digit_digit
                                        \.                      # dot
                                        eeg$""",                # extension
                                        re.VERBOSE)

        list_filesExtension_eeg : List[str] = Eeg.get_properFileList(searchPattern, pathFolder_testEegRaw)
        print(f"{list_filesExtension_eeg}\n")
        ##
        searchPattern = re.compile(r""" ^(ad_)                  # start str
                                        [ae]                    # a or e  
                                        ( (\d) | (\d_\d) )      # some digit or digit_digit
                                        \.                      # dot
                                        vhdr$""",               # extension
                                        re.VERBOSE)

        list_filesExtension_vhdr : List[str] = Eeg.get_properFileList(searchPattern, pathFolder_testEegRaw)
        print(f"{list_filesExtension_vhdr}\n")
        ##
        searchPattern = re.compile(r""" ^(ad_)                  # start str
                                        [ae]                    # a or e  
                                        ( (\d) | (\d_\d) )      # some digit or digit_digit
                                        \.                      # dot
                                        vmrk$""",               # extension
                                        re.VERBOSE)

        list_filesExtension_vmrk : List[str] = Eeg.get_properFileList(searchPattern, pathFolder_testEegRaw)
        print(f"{list_filesExtension_vmrk}\n")
        
        return list_filesExtension_eeg, list_filesExtension_vhdr, list_filesExtension_vmrk
#list_filesExtension_eeg, list_filesExtension_vhdr, list_filesExtension_vmrk = Eeg.testVrvrakk_searchRawFiles()



