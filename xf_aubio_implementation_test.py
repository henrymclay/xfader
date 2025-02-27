########################################################################
# tests for xfader.py
# by: Henry Clay
# using pytest
# alternate algorithm from aubio library, hopefully will do better with breakbeats
#
########################################################################

import pytest
import xfader 
import os
from pydub import AudioSegment 
from pydub.playback import play

from aubio import source, tempo
from numpy import median, diff

#this is basically out of the examples from the docs
def get_file_bpm(path):
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512

    s = aubio.source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = aubio.tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            print("not enough beats found in {:s}".format(path))
            return 0

    return beats_to_bpm(beats, path)


def test_aubio():
    return

def bpm_test_runner(path):
    dir = os.listdir(path)

    for filename in dir:
        wav = path + filename
        tempo_int = get_file_bpm(wav)
        #bpm = int(tempo_list[0][0])
        if tempo_int > 160 : 
            tempo_int = tempo_int / 2
        elif tempo_int < 70 : 
            tempo_int = tempo_int * 2
        print(filename, str(":"), str(tempo_int))
    return


test_aubio()