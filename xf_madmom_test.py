########################################################################
# tests for xfader.py
# by: Henry Clay
# using pytest
# alternate approach using an algorithm from madmom library 
# leverages ML model 
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

def test_madmom(wav, tempo_min = 70, tempo_max = 160):
    # Use madmom's BeatTrackingProcessor to estimate the BPM
    # needs fps parameter or it errors 
    # 100 is correct, seems to be default value (not 100% clear in madmom docs)
    proc = madmom.features.tempo.TempoEstimationProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(wav)
    bpm_list = proc(act)

    # this is returning a list of floats, not an int, so lets get the first result as an int
    tempo = int(bpm_list[0][0])
    # these keep the answers reasonable, as half/double time estimations are common 
    # default values are between 70 and 160 though this has been refactored to take other values
    if tempo > tempo_max : 
        tempo = tempo / 2
    elif tempo < tempo_min : 
        tempo = tempo * 2
    return tempo

def bpm_test_runner(path):
    dir = os.listdir(path)

    for filename in dir:
        wav = path + filename
        tempo = test_madmom(wav)
        
        print(filename, str(":"), str(tempo))
    return


bpm_test_runner("./test_data/r2/")

