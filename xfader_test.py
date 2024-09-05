########################################################################
# unit tests for xfader.yp
# by: Henry Clay
# using pytest
########################################################################


########################################################################
#
#
#
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
########################################################################


sample = AudioSegment.from_wav('./test_data/James_Brown_-_Funky_President.wav') 
play(sample) #original sample, which is X @ X bpm, should play 
play(xfader.repitch(106 , 160, sample)) # pitched sample, which is X @ X bpm, should play 

