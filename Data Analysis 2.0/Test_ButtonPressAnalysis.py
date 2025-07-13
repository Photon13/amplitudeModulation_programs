import os
from pathlib import Path
from typing import List
import re

pathFile : Path = Path("button press files\\preTest_participant0.vmrk")

with open(pathFile, "r") as f:
    lines : List[str] = f.readlines()

for i in range(0,11):
    lines.pop(0)

print("\n")
print(lines)

sampleRate = 500
# 1 Sekunde = 500 Samples

pre_AMP_RISE_LIST = [0.186, 0.0, 0.0, 0.0, 0.0, 0.0, 0.258, 0.0, 0.0, 0.186, 0.0, 0.0, 0.0, 0.0, 0.0, 0.366, 0.0, 0.0, 0.33, 0.0, 0.0, 0.258, 0.0, 0.0, 0.0, 0.0, 0.0, 0.186, 0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.33, 0.0, 0.0, 0.0, 0.0, 0.0, 0.258, 0.0, 0.0, 0.0, 0.0, 0.0, 0.294, 0.0, 0.0, 0.366, 0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.294, 0.0, 0.0, 0.366, 0.0, 0.0, 0.0, 0.0, 0.0, 0.186, 0.0, 0.0, 0.366, 0.0, 0.0, 0.0, 0.0, 0.0, 0.294, 0.0, 0.0, 0.366, 0.0, 0.0, 0.186, 0.0, 0.0, 0.0, 0.0, 0.0, 0.366, 0.0, 0.0, 0.366, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.402, 0.0, 0.0, 0.33, 0.0, 0.0, 0.186, 0.0, 0.0, 0.15, 0.0, 0.0, 0.33, 0.0, 0.0, 0.0, 0.0, 0.0, 0.366, 0.0, 0.0, 0.258, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.258, 0.0, 0.0, 0.366, 0.0, 0.0, 0.0, 0.0, 0.0, 0.294, 0.0, 0.0, 0.294, 0.0, 0.0, 0.0, 0.0, 0.0, 0.402, 0.0, 0.0, 0.402, 0.0, 0.0, 0.222, 0.0, 0.0, 0.33, 0.0, 0.0, 0.402, 0.0, 0.0, 0.0, 0.0, 0.0, 0.222, 0.0, 0.0, 0.222, 0.0, 0.0, 0.186, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.294, 0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.0, 0.0, 0.0, 0.258, 0.0, 0.0, 0.402, 0.0, 0.0, 0.186, 0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.222, 0.0, 0.0, 0.0, 0.0, 0.0, 0.33, 0.0, 0.0, 0.402, 0.0, 0.0, 0.294, 0.0, 0.0, 0.294, 0.0, 0.0, 0.0, 0.0, 0.0, 0.222, 0.0, 0.0, 0.0, 0.0, 0.0, 0.258, 0.0, 0.0, 0.0, 0.0, 0.0, 0.402, 0.0, 0.0, 0.222, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.0, 0.0, 0.258, 0.0, 0.0, 0.222, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.366, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.402, 0.0, 0.0, 0.402, 0.0, 0.0, 0.222, 0.0, 0.0, 0.402, 0.0, 0.0, 0.15, 0.0, 0.0, 0.258, 0.0, 0.0, 0.294, 0.0, 0.0, 0.222, 0.0, 0.0, 0.15, 0.0, 0.0, 0.294, 0.0, 0.0, 0.0, 0.0, 0.0, 0.186, 0.0, 0.0, 0.186, 0.0, 0.0, 0.258, 0.0, 0.0, 0.0, 0.0, 0.0, 0.222, 0.0, 0.0, 0.0, 0.0, 0.0]

ampRises = []
for zahl in pre_AMP_RISE_LIST:
    if zahl not in ampRises:
        ampRises.append(zahl)

ampRises.sort()
ampRises.remove(0.0)

ampRiseDict : dict = {}
for aR in ampRises:
    ampRiseDict[f"{aR}"] = 0



zeitenMarker_shiftLeft_samples : List[List] = []
zeitenMarker_buttons_samples : List[List] = []

zeitzBus_samples = int( re.findall(r"\d+", lines[1])[2] )

for l in lines:
    if( "S 32" in l):
        time = int( re.findall(r"\d+", l)[2] )
        zeitenMarker_shiftLeft_samples.append( time - zeitzBus_samples )

for l in lines:
    if( "S128" in l):
        time = int( re.findall(r"\d+", l)[2] )
        zeitenMarker_buttons_samples.append( time - zeitzBus_samples )

zeitenMarker_shiftLeft_sec : List[List] = []
zeitenMarker_buttons_sec : List[List] = []

for e in zeitenMarker_shiftLeft_samples:
    zeitenMarker_shiftLeft_sec.append( e / sampleRate )

for e in zeitenMarker_buttons_samples:
    zeitenMarker_buttons_sec.append( e / sampleRate )


pre_AMP_RISE_LIST_nurShifts = []
for e in pre_AMP_RISE_LIST:
    if( e != 0.0):
        pre_AMP_RISE_LIST_nurShifts.append(e)


zeitenAmpRises : dict = {}

for aR in ampRises:
    zeitenAmpRises[f"{aR}"] = []

for i in range( len(pre_AMP_RISE_LIST_nurShifts)):
    aR = pre_AMP_RISE_LIST_nurShifts[i]
    t = zeitenMarker_shiftLeft_sec[i]
    zeitenAmpRises[f"{aR}"].append(t)

for key in zeitenAmpRises:
    print(key, end = " ")
    print(zeitenAmpRises[f"{key}"])