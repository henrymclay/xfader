#!

#########################################################################
# xfader - an audio sample manipulation and crossfading utility
# v 0.0.2: takes a target and a bpm and re-pitches + exports at that bpm 
# by H. Clay 
# 2024
#########################################################################

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

def sample_export(sample:AudioSegment, path):
    output = sample.export(path, "wav")
    return output

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
# repitch(AudioSegment, int, int, int): re-pitching function
# calculates the ratio between starting and target bpm, then resamples at 
# that sample rate. returns the pitched (up or down) segment
##########################################################################

def repitch(in_segment, in_tempo, out_tempo, out_rate = 44100):
    # start it out by getting the ratio of old to new bpm and use it to generate the new sample rate
    bpm_ratio = out_tempo / in_tempo
    new_sample_rate = int(in_segment.frame_rate * bpm_ratio)
    #resamples the original at the new rate, i.e. plays it faster, then converts new sample to 441khz 
    pitched_segment = in_segment._spawn(in_segment.raw_data, overrides={'frame_rate': new_sample_rate})
    pitched_segment = pitched_segment.set_frame_rate(out_rate)
    return pitched_segment

##########################################################################
# main: the main function
# takes a bpm and a path to a sample to manipulate
# exports in the same folder
##########################################################################

def main():
    if len(sys.argv) == 3:
        print("xfading...")
        file = sys.argv[1]
        out_bpm = sys.argv[2]

        # we need bpm to be a number and file to be a wav or a path to a dir of wavs. 
        #first, check number
        if not out_bpm.isnumeric():
            print("bpm must be a number")
            exit
        # then, check that the path provided is either a .wav file or a directory. 
        # 44.1khz warning has no software check yet, just a user reminder
        # in light of the .wav check, isfile might be redundant
        elif not ( (os.path.isfile(file) and file.endswith(".wav") ) or os.path.isdir(file) ):
            print("issues with the path - needs to be a 44.1khz .wav file or a directory")
            exit
        else:
            # once we're sure we have a number and a .wav / dir...
            out_bpm = int(out_bpm)
            # if directory
            if os.path.isdir(file):
                dir = os.listdir(file)
                for filename in dir:
                    if filename.endswith(".wav"):
                        wavpath = file + filename
                        # detect tempo using madmom then import into pydub
                        tempo = bpm_detect(wavpath)
                        in_sample = sample_import(wavpath)       
                        # repitch        
                        pitched_sample = repitch(in_sample, tempo, out_bpm)
                        # generate new name e.g. think4.wav -> think4_160.wav, export
                        newname = wavpath[:(wavpath.find(".wav"))] + "_" + str(out_bpm) + ".wav"
                        sample_export(pitched_sample, newname) 
                        print(newname + " exported")
                    else: 
                        # if it's not a wav, don't do it 
                        print("skipped " + filename) 
                exit
            elif os.path.isfile(file): 
                # detect tempo using madmom then import into pydub
                tempo = bpm_detect(file)
                in_sample = sample_import(file)
                # repitch
                pitched_sample = repitch(in_sample, tempo, out_bpm)
                # generate new name e.g. think4.wav -> think4_160.wav, export
                newname = file[:(file.find(".wav"))] + "_" + str(out_bpm) + ".wav"
                sample_export(pitched_sample, newname) 
                print(newname + " exported")
                exit
            else: 
                print("bad path to file - this ia a weird one. make sure you provided the correct path")
                exit
                #in practice this branch should never come up, if this error is occurring something strange is happening
    else:
        print("bad args")
        print("expected: 'xfader [path/to/wav] [out_bpm]' ")
        exit

if __name__ == "__main__":
    main()


"""
TODO: 
script header for bash
file vs folder mode
export to different folder
new rename scheme
----
silence adder

"""