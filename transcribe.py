import os
import subprocess
import whisper
import torch
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tqdm import tqdm
import opencc

INPUT_FOLDER = "/home/meihan/trans/inputs"
OUTPUT_FOLDER = "/home/meihan/trans/outputs"
MODEL_SIZE = "medium"   


def ensure_output_folder():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_to_wav(input_file, output_file="temp.wav"):
    """Convert input audio to WAV using ffmpeg."""
    subprocess.run([
        "ffmpeg", "-y", "-i", input_file,
        "-ar", "16000", "-ac", "1", output_file
    ], check=True)
    return output_file


def transcribe_audio(audio_path, output_txt, model, device):
    """Transcribe one audio file to text using Whisper and show detected language."""
    wav_file = convert_to_wav(audio_path)

    print(f"🎙️ Transcribing {audio_path}...")

    # Run transcription (no progress_callback in vanilla whisper)
    result = model.transcribe(
        wav_file,
        verbose=True,
    )

    # Save stranscript
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"✅ Saved simplified transcript: {output_txt}")

    os.remove(wav_file)  # cleanup temp file


class AudioHandler(FileSystemEventHandler):
    def __init__(self, model, device):
        self.model = model
        self.device = device

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith((".mp3", ".wav", ".m4a", ".flac", ".ogg")):
            # Give time for file copy to finish
            time.sleep(1)
            output_txt = os.path.join(
                OUTPUT_FOLDER, os.path.splitext(os.path.basename(event.src_path))[0] + ".txt"
            )
            transcribe_audio(event.src_path, output_txt, self.model, self.device)


def main():
    ensure_output_folder()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading Whisper model '{MODEL_SIZE}' on {device}...")
    model = whisper.load_model(MODEL_SIZE, device=device)

    # Process existing files first
    for file in os.listdir(INPUT_FOLDER):
        if file.lower().endswith((".mp3", ".wav", ".m4a", ".flac", ".ogg")):
            input_path = os.path.join(INPUT_FOLDER, file)
            output_txt = os.path.join(OUTPUT_FOLDER, os.path.splitext(file)[0] + ".txt")
            transcribe_audio(input_path, output_txt, model, device)

    # Watch for new files
    event_handler = AudioHandler(model, device)
    observer = Observer()
    observer.schedule(event_handler, INPUT_FOLDER, recursive=False)
    observer.start()

    print(f"👀 Watching {INPUT_FOLDER} for new audio files...")
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
