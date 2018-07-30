"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
# sets up the portaudio system
p = pyaudio.PyAudio()

"""# define callback (2)"""
# To record or play audio, open a stream on the desired device with
# the desired audio parameters using pyaudio.PyAudio.open()
# This sets up a pyaudio.Stream to paly or record audio!
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)
	"""
	In callback mode, PyAudio will call this whenever it needs new audio
	data (to play) and/or when there is new (recorded) audio data available.
	Note that PyAudio calls the callback function in a separate thread.
	The function has the following signature:
callback(<input_data>, <frame_count>, <time_info>, <status_flag>)
	"""
# open stream using callback (3)
""" With this you can play audio by writing audio data to the stream
 """
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream() # pyaudio.Stream.start_stream()
"""Starts processing the audio stream using this #... which
will call the callback function repeatedly until that function
returns pyaudio.paComplete """


# wait for stream to finish (5)
while stream.is_active(): # Keeps stream active
    time.sleep(0.1) # Could try time.sleep(0.05)

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()
