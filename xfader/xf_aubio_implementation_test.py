########################################################################
# tests for xfader.py
# by: Henry Clay
# using pytest
# alternate algorithm from aubio library, hopefully will do better with breakbeats
#
########################################################################

import pytest
import xfader 
import numpy
from pydub import AudioSegment 
from pydub.playback import play


def bpm_detect_a(file):
    return file

def bpm_aubio_slow():
    tempo = xfader.bpm_detect('./test_data/James_Brown_-_Funky_President.wav')
    assert(tempo == 108)

def bpm_aubio_fast():

    tempo = xfader.bpm_detect('./test_data/Funky_President160.wav')
    assert(tempo == 160)


def test_aubio():

    return

test_aubio()