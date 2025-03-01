#########################################################################
# xfader - an audio sample manipulation and crossfading utility
# but v 0.0.1 is just a sample repitcher 
# by H. Clay 
# 2024
#########################################################################

# TODO
# better error messages
# bpm detection
# test coverage ******

import sys
import os
import ffmpeg
import madmom

from pydub import AudioSegment
from pydub.playback import play

##########################################################################
# sample_import(path) / sample_export(path) : sample import + export 
# takes wav file  (at provided path) and gets AudioSegment for pydub. 
# expects 44.1khz 16 bit wavs for now
##########################################################################

def sample_import(path):
    sample = AudioSegment.from_wav(path)
    return sample

def sample_export(sample, path):
    output = sample.export(path, "wav")
    return output

##########################################################################
# ad_prep(AudioSegment, hz: int, length:int) : takes audio data (pydub AudioSegment) and prepares it 
# to be analyzed. The goal is to make it into a more song-like form as that 
# is what our bpm detection algorithm expects. 
# Also, going to cut at 500hz in order to isolate the fundamentals of
# kick/snare/etc and eliminate noise + extraneous percussion
# this means: 
# - looping
# - filtering
# hz is hertz of filter frequency, length is length of "song" in ms
##########################################################################

def ad_prep(segment, hz = 500, length = 30000): 
    ad = segment.low_pass_filter(hz)
    count = 0
    while len(ad) < length :
        ad += ad
        count += 1
    return ad, count

##########################################################################
# bpm_detect(file path, int (default), int (default)): beat detection function
# detects the bpm of a sample based on peaks 
# librosa implementation almost from the docs 
# beat_frames will be nice to have when I get DTW going 
##########################################################################

def bpm_detect(wav, tempo_min = 70, tempo_max = 160):
    # Use madmom's BeatTrackingProcessor to estimate the BPM
    # needs fps parameter or it errors 
    # 100 is correct, seems to be default value (not 100% clear in madmom docs)
    proc = madmom.features.tempo.TempoEstimationProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(wav)
    # this is returning a 2D array of floats, not an int, so lets get the first result as an int
    bpm_list = proc(act)
    tempo = bpm_list[0][0]
    # these keep the answers reasonable, as half/double time estimations are common 
    # default values are between 70 and 160 though this has been refactored to take other values
    if tempo > tempo_max : 
        tempo = tempo / 2
    elif tempo < tempo_min : 
        tempo = tempo * 2
    #we do this after the mult/division to get less error
    tempo = int(tempo)
    return tempo

##########################################################################
# repitch(AudioSegment, bpm, bpm): re-pitching function
# calculates the ratio between starting and target bpm, then resamples at 
# that sample rate. returns the pitched (up or down) segment
##########################################################################

def repitch(in_segment, in_tempo, out_tempo):
    bpm_ratio = out_tempo / in_tempo
    new_sample_rate = int(in_segment.frame_rate * bpm_ratio)
    pitched_segment = in_segment._spawn(in_segment.raw_data, overrides={'frame_rate': new_sample_rate})
    pitched_segment = pitched_segment.set_frame_rate(44100)
    return pitched_segment

##########################################################################
# main: the main function
# scolds about arguments if those are bad
# the flow is: load samples in to process
# beat + bpm detection 
##########################################################################

def main():
    if len(sys.argv) == 3:
        print("xfading...")
        file = sys.argv[1]
        out_bpm = sys.argv[2]

        if not out_bpm.isnumeric():
            print("bpm must be a number")
            exit
        else:
            # input validation for sample file needed... 
            # detect tempo using madmom then import into pydub
            tempo = bpm_detect(file)
            in_sample = sample_import(file)
            # repitch
            out_bpm = int(out_bpm)
            pitched_sample = repitch(in_sample, tempo, out_bpm)
            # generate new name e.g. think4.wav -> think4_160.wav, export
            newname = file[:(file.find(".wav"))] + "_" + str(out_bpm) 
            sample_export(pitched_sample, newname) 
            print(newname + " exported")
            exit
    else:
        print("bad args")
        print("expected: 'xfader [path/to/wav] [out_bpm]' ")
        exit

if __name__ == "__main__":
    main()


"""
we need: 

main: 
    input validation: file to change, target tempo     
    - gets the file's bpm 
    - - gets the file's expected vs actual length
    - repitches the file to new bpm

"""