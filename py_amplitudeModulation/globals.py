from pathlib import Path
import os

_Version = "_V0_0_0"

#class GlobalPaths:
    
    #def getPaths():

path_cwd = os.getcwd()
# e.g. path_cwd = .../amplitudeModulation/amplitudeModulation_programs/amplitudeModulation_V0_0_0
path_test = os.path.join(path_cwd, f"test{_Version}")
# e.g. .../amplitudeModulation_V0_0_0/test_V0_0_0

print("Hallo {path_test}")

