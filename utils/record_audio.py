import pyaudio
import wave
import tempfile
import os
import threading


def record_audio():
    # Set parameters for recording
    chunk = 1024  # Buffer size
    format = pyaudio.paInt16  # Format for 16-bit audio
    channels = 1  # Mono audio
    rate = 44100  # Sample rate in Hz

    # Set up temporary directory and file path
    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, "temp_audio.wav")

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream for recording
    stream = p.open(
        format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk
    )

    print("Recording... Press Enter to stop.")

    frames = []
    recording = True  # Control flag for recording

    # Function to stop recording when Enter is pressed
    def stop_recording():
        input()  # Wait for Enter key press
        nonlocal recording
        recording = False  # Set the flag to False to stop recording

    # Start the stop_recording function in a separate thread
    stop_thread = threading.Thread(target=stop_recording)
    stop_thread.start()

    # Record until Enter is pressed
    try:
        while recording:
            data = stream.read(chunk)
            frames.append(data)
    finally:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded audio to a temporary file
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b"".join(frames))

        print(f"Audio recorded and saved to: {filename}")

    return filename  # Return the path to the recorded file
