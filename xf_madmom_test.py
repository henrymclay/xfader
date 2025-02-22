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
    # needs fps parameter or it errors 
    # not sure 100 is correct
    proc = madmom.features.tempo.TempoEstimationProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(wav)
    bpm = proc(act)

    return bpm

def bpm_test_runner(path):
    dir = os.listdir(path)

    for filename in dir:
        wav = path + filename
        tempo = test_madmom(wav)
        print(filename, str(":"), str(tempo))
    return


bpm_test_runner("./test_data/r2/")

