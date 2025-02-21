########################################################################
# tests for xfader.py
# by: Henry Clay
# using pytest
# alternate approach using an algorithm from madmom library 
# leverages LLM 
# not positive about deploying compactly 
# so unless it really works and the others don't...
# I'm not sure its the way
########################################################################

import pytest
import xfader 
import numpy
import madmom
import os
from pydub import AudioSegment 
from pydub.playback import play

def test_madmom(wav):
    # Use madmom's BeatTrackingProcessor to estimate the BPM
    bpm = madmom.features.beats.BeatTrackingProcessor(madmom.features.beats.RNNBeatProcessor()(wav))

    return bpm

def bpm_test_runner(path):
    directory = os.listdir(path)

    for filename in directory:
        file = path + filename
        tempo = test_madmom(file)
        print(filename, str(":"), str(tempo))
    return


bpm_test_runner("./test_data/r2/")

