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

amen1path = "./test_data/cutbreaks/Amen1.wav"
amen2path = "./test_data/cutbreaks/Amen2.wav"
amen4path = "./test_data/cutbreaks/Amen4.wav"
funky1path = "./test_data/cutbreaks/Funky1.wav"
funky2path = "./test_data/cutbreaks/Funky2.wav"
funky4path = "./test_data/cutbreaks/Funky4.wav"
amen_long_path = ".//test_data/cutbreaks/AmenLong.wav"
funky_long_path = "./test_data/cutbreaks/FunkyLong.wav"

break_paths = [amen1path, amen2path, amen4path, amen_long_path, funky1path, funky2path, funky4path, funky_long_path]
#break_paths = [amen1path, amen2path, amen4path, funky1path, funky2path, funky4path]

amen_bpm = 136
funky_bpm = 96

amen1 = xfader.sample_import(amen1path)
funky1 = xfader.sample_import(funky1path) 

#concats audio
amen_long = amen1 + amen1
funky_long = funky1 + funky1

amen_long += amen_long
funky_long += funky_long

xfader.sample_export(amen_long, amen_long_path)
xfader.sample_export(funky_long, funky_long_path)

print("Expected: Amen 138, Funky 101")

for path in break_paths:
    tempo = xfader.bpm_detect(path)
    print(path, str(":"), str(tempo))


"""
my takeaway here is that it really likes loops of 4 bars with windows of 32nds, or 1/8ths of the sample. 
I didn't get good results with 1 bar. Looping 1 bar to 4 seems to work, and 2 bars is ideal. I did get a half-tempo
error w/ the Amen but it's "right". 

If I window it at 80-150bpm, then I can start doing things like inferring # of bars based on samples 
And thats an easy correction
"""







