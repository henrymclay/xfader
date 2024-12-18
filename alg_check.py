#########################################################################
# Benchmarking for Python BPM detection algorithm 
#
# by H. Clay 
# 2024
#########################################################################

import pytest
import xfader 
import numpy
from pydub import AudioSegment 

import os

paths = os.listdir("./test_data/r2/")

for path in paths:
    file = "./test_data/r2/" + path
    loop = xfader.sample_import(file)
    tempo = xfader.get_tempo(loop)
    print(path, str(":"), str(tempo))

