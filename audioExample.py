# Should be Blocking Mode Audio I/O.py example
"""
PyAudio Example: Play a wave file.
"""

import pyaudio
import wave
import sys

CHUNK =1024

if len(sys.argv) < 2:
    print ("Plays a wave file.\n\nUsage: % filename.wav" % filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)

# read data
data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()

"""
(1) To use PyAudio, first instantiate PyAudio using pyaudio.PyAudio() which sets up the portaudio system.

(2) To record or play audio, open a stream on the desired device with the desired
audio parameters using pyaudio.PyAudio.open()
	This sets up the pyaudio.Stream to play or record audio

(3) Play audio by writing audio data to the stream using pyaudio.Stream.write(),
or read audio data from the stream using pyaudio.Stream.read().
	Note: While in "blocking mode", each pyaudio.Stream.write() or
		pyaudio.Stream.read() blocks until all the given/requested
		frames have been played recorded.
		Alternatively, to generate audio data on the fly or immediately
		process recorded audio data, use the "callback mode" outlined
		below.

(4) Use pyaudio.Stream.stop_stream() to pause palying/recording, and
	pyaudio.Stream.close() to termiante the stream.

(5) Finally, terminate the portaudio session using pyaudio.PyAudio.terminate().
"""




