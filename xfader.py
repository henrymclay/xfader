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
import librosa
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
# ad_prep(segment) : takes audio data (pydub AudioSegment) and prepares it 
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
# bpm_detect(file): beat detection function
# detects the bpm of a sample based on peaks 
# librosa implementation almost from the docs 
# beat_frames will be nice to have when I get DTW going 
##########################################################################

def bpm_detect(sample_file, count):
    audio, rate = librosa.load(sample_file)
    hop = round(rate * len(sample_file) * 1/count * 1/4096) # hop length of 64ths of original 
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=rate, hop_length=hop)
    bpm = tempo[0] # this seems to be a one member array...
    bpm = round(bpm)
    return bpm

##########################################################################
# repitch(bpm, bpm, segment): re-pitching function
# calculates the ratio between starting and target bpm, then resamples at 
# that sample rate. returns the pitched (up or down) segment
##########################################################################

    
def repitch(in_tempo, out_tempo, in_segment):
    bpm_ratio = out_tempo / in_tempo
    new_sample_rate = int(in_segment.frame_rate * bpm_ratio)
    pitched_segment = in_segment._spawn(in_segment.raw_data, overrides={'frame_rate': new_sample_rate})
    pitched_segment = pitched_segment.set_frame_rate(44100)
    return pitched_segment

##########################################################################
# get_tempo(segment) : 
# wrapper for bpm detection that does the loading buffering deleting  
# it is very clunky to bounce the wav and then re-load it but that's what
# the modules prefer
##########################################################################

def get_tempo(sample):
    loop, count = ad_prep(sample)
    sample_export(loop, "./loop.wav")
    #bounce = sample_import("./loop.wav")
    tempo = bpm_detect("./loop.wav", count)
    if os.path.exists("./loop.wav"):
        os.remove("./loop.wav")
    return tempo

##########################################################################
# main: the main function
# scolds about arguments if those are bad
# the flow is: load samples in to process
# beat + bpm detection 
##########################################################################

def main():
    if len(sys.argv) == 2:
        print("xfading...")
        file = sys.argv[0]
        out_bpm = sys.argv[1]

        if  not out_bpm.isnumeric():
            print("bpm must be a number")
            exit
        else:
            #input validation for sample file needed... 
            loop = sample_import(file)
            tempo = get_tempo(loop)
            #add: re-pitching 
            pitched_sample = repitch(loop, tempo, out_bpm)
            #e.g. think4.wav -> think4_160.wav
            newname = file[:(file.find(".wav"))] + "_" + str(out_bpm) 
            sample_export(pitched_sample, newname)
            print(newname + " exported")
            exit
    else:
        print("bad args")
        print("expected: 'xfader [path/to/file] [out_bpm]' ")
        exit

if __name__ == "__main__":
    main()
