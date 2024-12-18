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

######################################################################
# ad_prep test 
# checks that the audio is being processed correctly  
# imports sample, runs the prep function (filters + loops), exports, re-imports and checks attrs of imported file
######################################################################

def ad_prep_test(): 
    song_test = xfader.sample_import('./test_data/crunch/James_Brown_-_Funky_President.wav')
    song_test = xfader.ad_prep(song_test)
    xfader.sample_export(song_test, './test_data/crunch/long_test.wav')
    long_test = xfader.sample_import('./test_data/crunch/long_test.wav')
    assert(len(long_test) > 120000)
    #play(long_test)


######################################################################
# filter_bpm_test(): 
# checks the bpm detection when using the filter->loop process
######################################################################

def filter_bpm_test(): 
    loop = xfader.sample_import('./test_data/r2/Juice_-_Catch_A_Groove.2bar.108bpm.wav')
    loop = xfader.ad_prep(loop)
    xfader.sample_export(loop, './test_data/crunch/long_bpm_test.wav')
    tempo = xfader.bpm_detect('./test_data/crunch/long_bpm_test.wav')
    print(str("Expected: 108 Analyzed: "), str(tempo))
    assert(tempo == 108)

########################################################################
# TODO: 
# import repitch export and compare to pre-rendered
# detection on known info
########################################################################

########################################################################
# tests get run here
########################################################################

#ad_prep_test()
filter_bpm_test()
#play_test()
#import_export_test()
#bpm_test1()
#bpm_test2()