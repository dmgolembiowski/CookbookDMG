"""
pyaudio.get_format_from_width(width, unsigned=True)
Returns a PortAudio format constant for the specified width.
Parameters:	
width – The desired sample width in bytes (1, 2, 3, or 4)
unsigned – For 1 byte width, specifies signed or unsigned format.
Raises:ValueError – when invalid width
Return type:A PortAudio Sample Format constant

pyaudio.get_portaudio_version()
Returns portaudio version.
Return type:string

pyaudio.get_portaudio_version_text()
Returns PortAudio version as a text string.
Return type:	string

pyaudio.get_sample_size(format)
Returns the size (in bytes) for the specified sample format.
Parameters:	format – A PortAudio Sample Format constant.
Raises:	ValueError – on invalid specified format.
Return type:	integer
pyaudio.paAL = 9
Open Audio Library

$$pyaudio.paALSA = 8
$$Advanced Linux Sound Architecture (Linux only)

$$pyaudio.paASIO = 3
Steinberg Audio Stream Input/Output

pyaudio.paAbort = 2
An error ocurred, stop playback/recording

pyaudio.paBeOS = 10
BeOS Sound System

pyaudio.paComplete = 1
This was the last block of audio data

pyaudio.paContinue = 0
There is more audio data to come

pyaudio.paCoreAudio = 5
CoreAudio (OSX only)

pyaudio.paCustomFormat = 65536
a custom data format

pyaudio.paDirectSound = 1
DirectSound (Windows only)

pyaudio.paFloat32 = 1
32 bit float

pyaudio.paInDevelopment = 0
Still in development

pyaudio.paInputOverflow = 2
Buffer overflow in input

pyaudio.paInputUnderflow = 1
Buffer underflow in input

pyaudio.paInt16 = 8
16 bit int

pyaudio.paInt24 = 4
24 bit int

pyaudio.paInt32 = 2
32 bit int

pyaudio.paInt8 = 16
8 bit int

pyaudio.paJACK = 12
JACK Audio Connection Kit

pyaudio.paMME = 2
Multimedia Extension (Windows only)

pyaudio.paNoDevice = -1
Not actually an audio device

$$pyaudio.paOSS = 7
$$Open Sound System (Linux only)

pyaudio.paOutputOverflow = 8
Buffer overflow in output

pyaudio.paOutputUnderflow = 4
Buffer underflow in output

pyaudio.paPrimingOutput = 16
Just priming, not playing yet

pyaudio.paSoundManager = 4
SoundManager (OSX only)

pyaudio.paUInt8 = 32
8 bit unsigned int

pyaudio.paWASAPI = 13
Windows Vista Audio stack architecture

pyaudio.paWDMKS = 11
Windows Driver Model (Windows only)

Class PyAudio
class pyaudio.PyAudio
Python interface to PortAudio. Provides methods to:
initialize and terminate PortAudio
open and close streams
query and inspect the available PortAudio Host APIs
query and inspect the available PortAudio audio devices
Use this class to open and close streams.

Stream Management
open(), close()
Host API
get_host_api_count(), get_default_host_api_info(), get_host_api_info_by_type(), get_host_api_info_by_index(), get_device_info_by_host_api_device_index()
Device API
get_device_count(), is_format_supported(), get_default_input_device_info(), get_default_output_device_info(), get_device_info_by_index()
Stream Format Conversion
get_sample_size(), get_format_from_width()
Details

__init__()
Initialize PortAudio.

close(stream)
Close a stream. Typically use
$$Stream.close() instead.

Parameters:	stream – An instance of the Stream object.
Raises:	ValueError – if stream does not exist.
get_default_host_api_info()
Return a dictionary containing the default Host API parameters. The keys of the dictionary mirror the data fields of PortAudio’s PaHostApiInfo structure.

Raises:	IOError – if no default input device is available
Return type:	dict
get_default_input_device_info()
Return the default input Device parameters as a dictionary. The keys of the dictionary mirror the data fields of PortAudio’s PaDeviceInfo structure.

Raises:	IOError – No default input device available.
Return type:	dict
get_default_output_device_info()
Return the default output Device parameters as a dictionary. The keys of the dictionary mirror the data fields of PortAudio’s PaDeviceInfo structure.

Raises:	IOError – No default output device available.
Return type:	dict
get_device_count()
Return the number of PortAudio Host APIs.

Return type:	integer
get_device_info_by_host_api_device_index(host_api_index, host_api_device_index)
Return a dictionary containing the Device parameters for a given Host API’s n’th device. The keys of the dictionary mirror the data fields of PortAudio’s PaDeviceInfo structure.

Parameters:	
host_api_index – The Host API index number
host_api_device_index – The n’th device of the host API
Raises:	
IOError – for invalid indices

Return type:	
dict

get_device_info_by_index(device_index)
Return the Device parameters for device specified in device_index as a dictionary. The keys of the dictionary mirror the data fields of PortAudio’s PaDeviceInfo structure.

Parameters:	device_index – The device index
Raises:	IOError – Invalid device_index.
Return type:	dict
get_format_from_width(width, unsigned=True)
Returns a PortAudio format constant for the specified width.

Parameters:	
width – The desired sample width in bytes (1, 2, 3, or 4)
unsigned – For 1 byte width, specifies signed or unsigned format.
Raises:	
ValueError – for invalid width

Return type:	
A PortAudio Sample Format constant.

get_host_api_count()
Return the number of available PortAudio Host APIs.

Return type:	integer
get_host_api_info_by_index(host_api_index)
Return a dictionary containing the Host API parameters for the host API specified by the host_api_index. The keys of the dictionary mirror the data fields of PortAudio’s PaHostApiInfo structure.

Parameters:	host_api_index – The host api index
Raises:	IOError – for invalid host_api_index
Return type:	dict
get_host_api_info_by_type(host_api_type)
Return a dictionary containing the Host API parameters for the host API specified by the host_api_type. The keys of the dictionary mirror the data fields of PortAudio’s PaHostApiInfo structure.

Parameters:	host_api_type – The desired PortAudio Host API
Raises:	IOError – for invalid host_api_type
Return type:	dict
get_sample_size(format)
Returns the size (in bytes) for the specified sample format (a PortAudio Sample Format constant).

Parameters:	format – A PortAudio Sample Format constant.
Raises:	ValueError – Invalid specified format.
Return type:	integer
is_format_supported(rate, input_device=None, input_channels=None, input_format=None, output_device=None, output_channels=None, output_format=None)
Check to see if specified device configuration is supported. Returns True if the configuration is supported; throws a ValueError exception otherwise.

Parameters:	
rate – Specifies the desired rate (in Hz)
input_device – The input device index. Specify None (default) for half-duplex output-only streams.
input_channels – The desired number of input channels. Ignored if input_device is not specified (or None).
input_format – PortAudio sample format constant defined in this module
output_device – The output device index. Specify None (default) for half-duplex input-only streams.
output_channels – The desired number of output channels. Ignored if input_device is not specified (or None).
output_format – PortAudio Sample Format constant.
Return type:	
bool

Raises:	
ValueError – tuple containing (error string, PortAudio Error Code).

open(*args, **kwargs)
Open a new stream. See constructor for Stream.__init__() for parameter details.

Returns:	A new Stream
terminate()
Terminate PortAudio.

Attention:	Be sure to call this method for every instance of this object to release PortAudio resources.
Class Stream
class pyaudio.Stream(PA_manager, rate, channels, format, input=False, output=False, input_device_index=None, output_device_index=None, frames_per_buffer=1024, start=True, input_host_api_specific_stream_info=None, output_host_api_specific_stream_info=None, stream_callback=None)
PortAudio Stream Wrapper. Use PyAudio.open() to make a new Stream.

Opening and Closing
__init__(), close()
Stream Info
get_input_latency(), get_output_latency(), get_time(), get_cpu_load()
Stream Management
start_stream(), stop_stream(), is_active(), is_stopped()
Input Output
write(), read(), get_read_available(), get_write_available()
__init__(PA_manager, rate, channels, format, input=False, output=False, input_device_index=None, output_device_index=None, frames_per_buffer=1024, start=True, input_host_api_specific_stream_info=None, output_host_api_specific_stream_info=None, stream_callback=None)
Initialize a stream; this should be called by PyAudio.open(). A stream can either be input, output, or both.

Parameters:	
PA_manager – A reference to the managing PyAudio instance
rate – Sampling rate
channels – Number of channels
format – Sampling size and format. See PortAudio Sample Format.
input – Specifies whether this is an input stream. Defaults to False.
output – Specifies whether this is an output stream. Defaults to False.
input_device_index – Index of Input Device to use. Unspecified (or None) uses default device. Ignored if input is False.
output_device_index – Index of Output Device to use. Unspecified (or None) uses the default device. Ignored if output is False.
frames_per_buffer – Specifies the number of frames per buffer.
start – Start the stream running immediately. Defaults to True. In general, there is no reason to set this to False.
input_host_api_specific_stream_info –
Specifies a host API specific stream information data structure for input.

See PaMacCoreStreamInfo.

output_host_api_specific_stream_info –
Specifies a host API specific stream information data structure for output.

See PaMacCoreStreamInfo.

stream_callback –
Specifies a callback function for non-blocking (callback) operation. Default is None, which indicates blocking operation (i.e., Stream.read() and Stream.write()). To use non-blocking operation, specify a callback that conforms to the following signature:

callback(in_data,      # recorded data if input=True; else None
         frame_count,  # number of frames
         time_info,    # dictionary
         status_flags) # PaCallbackFlags
time_info is a dictionary with the following keys: input_buffer_adc_time, current_time, and output_buffer_dac_time; see the PortAudio documentation for their meanings. status_flags is one of PortAutio Callback Flag.

The callback must return a tuple:

(out_data, flag)
out_data is a byte array whose length should be the (frame_count * channels * bytes-per-channel) if output=True or None if output=False. flag must be either paContinue, paComplete or paAbort (one of PortAudio Callback Return Code). When output=True and out_data does not contain at least frame_count frames, paComplete is assumed for flag.

Note: stream_callback is called in a separate thread (from the main thread). Exceptions that occur in the stream_callback will:

print a traceback on standard error to aid debugging,
queue the exception to be thrown (at some point) in the main thread, and
return paAbort to PortAudio to stop the stream.
Note: Do not call Stream.read() or Stream.write() if using non-blocking operation.

See: PortAudio’s callback signature for additional details: http://portaudio.com/docs/v19-doxydocs/portaudio_8h.html#a8a60fb2a5ec9cbade3f54a9c978e2710

Raises:	
ValueError – Neither input nor output are set True.

close()
Close the stream

get_cpu_load()
Return the CPU load. This is always 0.0 for the blocking API.

Return type:	float
get_input_latency()
Return the input latency.

Return type:	float
get_output_latency()
Return the output latency.

Return type:	float
get_read_available()
Return the number of frames that can be read without waiting.

Return type:	integer
get_time()
Return stream time.

Return type:	float
get_write_available()
Return the number of frames that can be written without waiting.

Return type:	integer
is_active()
Returns whether the stream is active.

Return type:	bool
is_stopped()
Returns whether the stream is stopped.

Return type:	bool
read(num_frames, exception_on_overflow=True)
Read samples from the stream. Do not call when using non-blocking mode.

Parameters:	
num_frames – The number of frames to read.
exception_on_overflow – Specifies whether an IOError exception should be thrown (or silently ignored) on input buffer overflow. Defaults to True.
Raises:	
IOError – if stream is not an input stream or if the read operation was unsuccessful.

Return type:	
string

start_stream()
Start the stream.

stop_stream()
Stop the stream. Once the stream is stopped, one may not call write or read. Call start_stream() to resume the stream.

write(frames, num_frames=None, exception_on_underflow=False)
Write samples to the stream. Do not call when using non-blocking mode.

Parameters:	
frames – The frames of data.
num_frames – The number of frames to write. Defaults to None, in which this value will be automatically computed.
exception_on_underflow – Specifies whether an IOError exception should be thrown (or silently ignored) on buffer underflow. Defaults to False for improved performance, especially on slower platforms.
Raises:	
IOError – if the stream is not an output stream or if the write operation was unsuccessful.

Return type:	
None

Platform Specific
Class PaMacCoreStreamInfo
class pyaudio.PaMacCoreStreamInfo(flags=None, channel_map=None)
Mac OS X-only: PaMacCoreStreamInfo is a PortAudio Host API Specific Stream Info data structure for specifying Mac OS X-only settings. Instantiate this class (if desired) and pass the instance as the argument in PyAudio.open() to parameters input_host_api_specific_stream_info or output_host_api_specific_stream_info. (See Stream.__init__().)

Note:	Mac OS X only.
PortAudio Mac Core Flags
paMacCoreChangeDeviceParameters, paMacCoreFailIfConversionRequired, paMacCoreConversionQualityMin, paMacCoreConversionQualityMedium, paMacCoreConversionQualityLow, paMacCoreConversionQualityHigh, paMacCoreConversionQualityMax, paMacCorePlayNice, paMacCorePro, paMacCoreMinimizeCPUButPlayNice, paMacCoreMinimizeCPU
Settings
get_flags(), get_channel_map()
__init__(flags=None, channel_map=None)
Initialize with flags and channel_map. See PortAudio documentation for more details on these parameters; they are passed almost verbatim to the PortAudio library.

Parameters:	
flags – PortAudio Mac Core Flags OR’ed together. See PaMacCoreStreamInfo.
channel_map – An array describing the channel mapping. See PortAudio documentation for usage.
get_channel_map()
Return the channel map set at instantiation.

Return type:	tuple or None

get_flags()
Return the flags set at instantiation.

Return type:	integer

"""
