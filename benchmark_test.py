#########################################################################
# Benchmarking for Python BPM detection algorithm 
#
# by H. Clay 
# 2024
#########################################################################

"""
This script should generate performance data for the bpm detection alogorithm used by xfader. 
We're gonna use Think, Amen, and Funky Drummer
We're gonna pass 4 and 8 bar versions of Think and Amen
We're gonna try looping the bars 
Expected BPM: 
Think: 
Amen: 
Funky
"""


import pytest
import xfader 
import numpy
from pydub import AudioSegment 
from pydub.playback import play

def loop_break(audio):
    audio += audio 

    return 


#import samples to test 

amen1path = ".test_data/Amen1.wav"
amen2path = ".test_data/Amen1.wav"
amen4path = ".test_data/Amen1.wav"
funky1path = ".test_data/Amen1.wav"
funky2path = ".test_data/Amen1.wav"
funky4path = ".test_data/Amen1.wav"
amen512path = "./test_data/Amen512.wav"
funky512path = "./test_data/Funky512.wav"

break_paths = [amen1path, amen2path, amen4path, amen512path, funky1path, funky2path, funky4path, funky512path]

amen_bpm = 136
funky_bpm = 96

amen4 = xfader.sample_import(amen4path)
funky4 = xfader.sample_import(funky4path) 

#concats audio, loops 10 times
amen_long = amen4
for x in range(128):
    amen_long += amen4

funky_long = funky4
for x in range(128):
    funky_long += funky4

xfader.sample_export(amen_long, amen512path)
xfader.sample_export(funky_long, funky512path)


for path in break_paths:
    tempo = xfader.bpm_detect(path)
    print(path, str(":"), str(tempo))









