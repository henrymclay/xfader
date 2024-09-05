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
from pydub import AudioSegment
from pydub.playback import play

##########################################################################
# : sample import + export functions
# takes wav file and gets AudioSegment for pydub. 
# expects 44.1khz 16 bit wavs for now
##########################################################################

def sample_import(path, format="wav"):
    sample = AudioSegment.from_wav(path)
    return sample

def sample_export(sample, path, output_format="wav"):
    output = sample.export(path, format=output_format)
    return output


##########################################################################
# : beat detection function
# detects the bpm of a sample based on peaks 
# expects a single measure of 4/4
# can be modified by suppliying 
##########################################################################

def bpm_detect(sample_file, quarters=4):
    bpm = 160
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
            newname = file[:(file.find(".wav"))] + "_" + str(bpm) 

            output = sample_export(pitched_sample, newname)
            print(newname + " exported")
            exit
    else:
        print("bad args")
        print("expected: 'xfader [path/to/file] [in bpm] [out_bpm]' ")
        exit

if __name__ == "__main__":
    main()
