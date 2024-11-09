"""
IMPORTANT:
    -set path_excel_json

"""

from pathlib import Path
import os

_Version = "_V0_0_0"

class GlobalPaths:
    
    def getPaths():

        path_cwd = os.getcwd()
        # e.g. path_cwd = .../amplitudeModulation/amplitudeModulation_programs/amplitudeModulation_V0_0_0
        
        path_rcx = os.path.join(path_cwd, f"rcx{_Version}")

        path_excel_json = os.path.join(path_cwd, f" ") # MUST BE CHANGED LATER !!!

        return path_cwd, path_rcx, path_excel_json

    def getTestPaths():
        path_cwd = os.getcwd()
        # e.g. path_cwd = .../amplitudeModulation/amplitudeModulation_programs/amplitudeModulation_V0_0_0
        
        path_test = os.path.join(path_cwd, f"test{_Version}")
        # e.g. .../amplitudeModulation_V0_0_0/test_V0_0_0
