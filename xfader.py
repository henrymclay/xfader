#########################################################################
# xfader - an audio sample manipulation and crossfading utility
# but v 0.0.1 is just a sample repitcher 
# by H. Clay 
# 2024
#########################################################################

# TODO
# better error messages
# real functions
# figure out how to change sample pitch


import sys
import ffmpeg

from pydub import AudioSegment

##########################################################################
# : sample import function
# takes wav file and gets AudioSegment for pydub. 
# expects 44.1khz 16 bit wavs for now
##########################################################################

def sample_import(path, format="wav"):
    
    sample = AudioSegment.from_wav(path)

    return sample



##########################################################################
# : sample import function
# takes wav file and gets AudioSegment for pydub. 
# expects 44.1khz 16 bit wavs for now
##########################################################################dwa

def sample_export(path, sample, output_format="wav"):
    
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
# takes a bpm target and a loop file to re-pitch to hit that target 
# detects bpm of the loop 
#
##########################################################################

def repitch(out_tempo, in_file):

    in_tempo = bpm_detect(in_file)

    out_file = in_file
    return out_file



##########################################################################
# main: the main function
# scolds about arguments if those are bad
# the flow is: load samples in to process
# beat + bpm detection 
##########################################################################

def main():

    #input validation here - gotta pass file and bpm and nothing else!

    if len(sys.argv) > 2:
        print("bad args")
        print("expected: 'xfader [bpm] [file]' ")
        exit
    elif len(sys.argv) < 2:
        print("bad args")
        print("expected: 'xfader [bpm] [file]' ")
        exit
    elif len(sys.argv) == 2:
        print("xfading...")
        bpm = sys.argv[0]
        file = sys.argv[1]

        if not bpm.isnumeric():
            print("bpm must be a number")
            exit
        else:
            #input validation for sample file here 
            sample = sample_import(file)
            newname = file[:(file.find(".wav"))] + str(bpm)

            output = sample_export(sample, newname)
            print("newname exported")
            exit

        # output = repitch(bpm, sample)

        exit
    else:
        print("main error")
        exit

if __name__ == "__main__":
    main()
