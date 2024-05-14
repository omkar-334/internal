import sys
import wave

import keyboard
import pyaudio

from model import Model

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
OUTPUT_FILENAME = "output.wav"


def initialize():
    p = pyaudio.PyAudio()
    INDEX = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if "stereo" in dev["name"].lower():
            INDEX = dev["index"]
            break

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=INDEX, frames_per_buffer=CHUNK)
    return p, stream


def save_file(p, frames):
    wf = wave.open(OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    return OUTPUT_FILENAME


def record_audio():
    p, stream = initialize()
    print("Recording. Press ESC to stop...")
    frames = []
    try:
        while True:
            sys.stdout.write(".")
            sys.stdout.flush()
            data = stream.read(CHUNK)
            frames.append(data)
            if keyboard.is_pressed("esc"):
                break
    finally:
        print("\nRecording stopped...")
        stream.stop_stream()
        stream.close()
        p.terminate()

    filename = save_file(p, frames)
    return filename


if __name__ == "__main__":
    model = Model()

    audio = record_audio()
    text = model.transcribe(audio)
    print(text)
    print("--------------------------")
    response = model.generate(text)
    print(response)
