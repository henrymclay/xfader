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
import aubio
import os
from pydub import AudioSegment 
from pydub.playback import play



def test_aubio():
    return

def bpm_test_runner(path):
    dir = os.listdir(path)

    for filename in dir:
        wav = path + filename
        tempo_list = test_aubio(wav)
        tempo = int(tempo_list[0][0])
        if tempo > 160 : 
            tempo = tempo / 2
        elif tempo < 70 : 
            tempo = tempo * 2
        print(filename, str(":"), str(tempo))
    return


test_aubio()