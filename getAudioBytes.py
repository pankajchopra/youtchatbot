import os

import pyglet as pyglet
import simpleaudio as simpleaudio
from gtts import gTTS
import io
import sounddevice as sd
import wave
from pydub import AudioSegment
import pyaudio
import numpy as np


# pip install ffmpeg-downloader
# ffdl install --add-path
# import warnings
# warnings.filterwarnings("ignore", category=RuntimeWarning)


def read_wav_using_pydub(filename: str):
    # Load the WAV file
    audio = AudioSegment.from_file(filename)

    # Convert to raw data
    raw_data = audio.raw_data

    # Get sample width, channels, and frame rate
    sample_width = audio.sample_width
    channels = audio.channels
    frame_rate = audio.frame_rate

    # Convert raw data to numpy array
    if sample_width == 1:
        dtype = np.uint8  # 8-bit audio
    elif sample_width == 2:
        dtype = np.int16  # 16-bit audio
    elif sample_width == 4:
        dtype = np.int32  # 32-bit audio
    else:
        raise ValueError("Unsupported audio format.")

    print(f"dtype:{dtype})")
    audio_data = np.frombuffer(raw_data, dtype=dtype)
    if channels > 1:
        audio_data = audio_data.reshape(-1, channels)

    # Print some information about the audio file
    print(f'Sample Width: {sample_width}')
    print(f'Channels: {channels}')
    print(f'Frame Rate: {frame_rate}')
    print(f'Audio Data: {audio_data[:10]}')  # Print first 10 samples
    print(f'Raw Data: {raw_data}')
    play_raw_data(raw_data=raw_data,sample_width = sample_width, channels=channels, frame_rate=frame_rate)
    return raw_data

def text_to_audio_data(text):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en', slow=False)
    # Create an in-memory file-like object
    audio_file = io.BytesIO()
    # Write the audio data to the in-memory file
    tts.write_to_fp(audio_file)
    # Get the audio bytes from the in-memory file
    audio_bytes = audio_file.getvalue()
    return audio_bytes


def read_wav(filename: str):
    with wave.open(filename, 'rb') as wav_file:
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        comp_type = wav_file.getcomptype()
        comp_name = wav_file.getcompname()

        print(f'Number of Channels: {n_channels}')
        print(f'Sample Width: {sample_width}')
        print(f'Frame Rate: {frame_rate}')
        print(f'Number of Frames: {n_frames}')
        print(f'Compression Type: {comp_type}')
        print(f'Compression Name: {comp_name}')


def read_raw_audio_data(raw_audio_data: bytes):
    if len(raw_audio_data) % 2 != 0:
        # Handle the error appropriately (e.g., pad or truncate the data)
        print("Error: Raw audio data length is not a multiple of 2 bytes.")
        padded_length = (len(raw_audio_data) // 2) * 2
        padded_raw_audio_data = raw_audio_data[:padded_length]
        # Convert raw audio data to numpy array
        audio_data = np.frombuffer(padded_raw_audio_data, dtype=np.int16)
    else:
        # Convert raw audio data to numpy array
        audio_data = np.frombuffer(raw_audio_data, dtype=np.int16)
        print("Successfully converted raw audio data.")

    sd.play(audio_data, samplerate=44100)
    sd.wait()

    # # Determine the number of frames
    # num_frames = len(audio_data) // channels
    #
    # # Calculate duration
    # duration = num_frames / sample_rate
    #
    # print(f"Sample Rate: {sample_rate} Hz")
    # print(f"Channels: {channels}")
    # print(f"Number of Frames: {num_frames}")
    # print(f"Duration: {duration:.2f} seconds")
    num_frames = 44100/1024;
    return 44100, 1, 43, 5

def play_raw_data(raw_data, sample_width, channels, frame_rate ):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=frame_rate,
                    output=True)

    # Play the audio
    stream.write(raw_data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()


def play_raw_audio_data(raw_audio_data):
    # Define the sample rate and number of channels
    sample_rate = 44100
    channels = 1

    # Convert raw audio data to numpy array
    audio_data = np.frombuffer(raw_audio_data, dtype=np.int16)

    # Play the audio stream
    sd.play(audio_data, samplerate=sample_rate, channels=channels)
    sd.wait()  # Wait until playback is finished


# read_wav("../audio/1ch-mono.wav")
# text_to_audio_data("Hello Hello Testing Testing")
# read_wav_using_pydub("1ch-mono.wav")
# f = wave.open(audio_bytes, "rb")
# print(f.getnframes())
# print(f.readframes())
# audio_data = simpleaudio.PlayObject(audio_bytes)
# sd.play(data=audio_data, samplerate=16000)
#
# # Convert the audio bytes to an AudioSegment object
# audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
#
# # Set the sample rate to 16000 Hz
# audio_segment = audio_segment.set_frame_rate(16000)
#
# # Export the audio segment to bytes at the desired sample rate
# audio_bytes_16k = audio_segment.raw_data
# f = wave.open(audio_bytes_16k, "rb")
# print(f"16k:{f.getnframes()}")
# print(f"16k bytes:{f.readframes()}")
# # Optionally, you can save the audio to a file
# # tts.save("hello.mp3")
#
# # Print the type and length of the audio bytes
# print(f"Audio bytes are: {audio_bytes_16k}")
# print(f"Audio bytes type: {type(audio_bytes_16k)}")
# print(f"Audio bytes length: {len(audio_bytes_16k)}")