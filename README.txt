This is xfader, a python tool for manipulating audio samples of breakbeat loops for musical purposes. 

Right now, it's a script you can run from the command line: 

'xfader [path/to/file] [in bpm] [out_bpm]'

This will take a sample at the supplied path and expected 'in bpm', and re-time it to the 'out bpm'
using a resampling algorithm (like on typical music samplers and programs), just focussed on tempo 
rather than semitones for the output. 

Eventually, the functionalities will be expanded including:
- recursion over a folder vs an individual file
- tempo detection
- automatic quantization 
- smart sample cross-fading 

and many more!

