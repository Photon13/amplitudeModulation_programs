from pathlib import Path
import os

_Version = "_V0_0_0"

class GlobalPaths:
    
    def getPaths():

        path_cwd = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\amplitudeModulation_programs\\py_amplitudeModulation")

        path_json_excel = Path("d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\participantInformation")
        path_json = path_json_excel / "json"
        path_excel = path_json_excel / "excel"

        return path_cwd, path_json_excel, path_excel, path_json

class GlobalsSound:

    def getGlobalsSound():
        fAM_A = int(5)
        fAM_B = int(13)
        fAM_C = int(21)
        shift = int(4)
        return fAM_A, fAM_B, fAM_C, shift

class GlobalsBlocks:
    n_subblocks = int(1+30) # No shift, 30*shift
    n_blocks = int(2+16) # Test single_speaker=target, Test both=target, 16*normal_blocks
