########################################################################
# unit tests for xfader.yp
# by: Henry Clay
# using pytest
# pydub (the module) is throwing warnings 
########################################################################

import pytest
import xfader 
import numpy
from pydub import AudioSegment 
from pydub.playback import play

########################################################################
# repitch() tests
#
# very basic test to make sure repitch fires. verify by ear
# if you're running these on your machine you're gonna have to supply a testwav
########################################################################

def play_test():
    sample = AudioSegment.from_wav('./test_data/James_Brown_-_Funky_President.wav') 
    play(sample) #original sample, which is X @ X bpm, should play 
    play(xfader.repitch(106 , 160, sample)) # pitched sample, which is X @ X bpm, should play 

#######################################################################
# import +  export tests
# imports, pitches up, exports, imports the export and compares 
########################################################################

def import_export_test():
    sample = xfader.sample_import('./test_data/James_Brown_-_Funky_President.wav')
    pitched = xfader.repitch(104, 160, sample)
    xfader.sample_export(pitched, './test_data/Funky_President160.wav')
    sample_2 = xfader.sample_import('./test_data/James_Brown_-_Funky_President160.wav')
    assert(pitched == sample_2)


#######################################################################
# bpm detection test 
# tests bpm detection before + after repitch 
#######################################################################

def bpm_test1():
    tempo1 = xfader.bpm_detect('./test_data/James_Brown_-_Funky_President.wav')
    assert(tempo1 == 108)

def bpm_test2():

    tempo2 = xfader.bpm_detect('./test_data/Funky_President160.wav')
    assert(tempo2 == 160)
########################################################################
# TODO: 
# import repitch export and compare to pre-rendered
# detection on known info
########################################################################

########################################################################
# tests get run here
########################################################################

play_test()
import_export_test()
bpm_test1()
bpm_test2()