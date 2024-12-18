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
# kick/snare/etc and eliminate noise + extraneous percussion and try
# downsampling to do the same + save buffer space 
# this means: 
# 
# - looping
# - filtering
# - downsampling 
# hz is hertz of filter frequency, length is length of "song" in ms
##########################################################################

def ad_prep(segment, hz = 500, length = 120000): 
    ad = segment.low_pass_filter(hz)
    #ad = ad.set_frame_rate(1000)
    while len(ad) < length :
        ad += ad

    return ad


##########################################################################
# : beat detection function
# detects the bpm of a sample based on peaks 
# librosa implementation almost from the docs 
# beat_frames will be nice to have when I get DTW going 
##########################################################################

def bpm_detect(sample_file):
    audio, rate = librosa.load(sample_file)
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=rate)
    bpm = tempo[0] # this seems to be a one member array...
    bpm = round(bpm)
    return bpm

##########################################################################
# : re-pitching function
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
# main: the main function
# scolds about arguments if those are bad
# the flow is: load samples in to process
# beat + bpm detection 
##########################################################################

def main():
    if len(sys.argv) == 3:
        print("xfading...")
        file = sys.argv[0]
        in_bpm = sys.argv[1]
        out_bpm = sys.argv[2]

        if (not in_bpm.isnumeric()) or (not out_bpm.isnumeric()):
            print("bpm must be a number")
            exit
        else:
            #input validation for sample file here 
            sample = sample_import(file)
            #add: bpm detection
            #add: re-pitching 
            pitched_sample = repitch(sample, in_bpm, out_bpm)
            #e.g. think4.wav -> think4_160.wav
            newname = file[:(file.find(".wav"))] + "_" + str(out_bpm) 

            output = sample_export(pitched_sample, newname)
            print(newname + " exported")
            exit
    else:
        print("bad args")
        print("expected: 'xfader [path/to/file] [in bpm] [out_bpm]' ")
        exit

if __name__ == "__main__":
    main()
