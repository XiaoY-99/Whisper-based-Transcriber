# Whisper Auto-Transcriber

A lightweight, folder-watching audio transcription tool powered by
OpenAI Whisper. This project automatically detects new audio files,
converts them to WAV using FFmpeg, transcribes them, and saves the
results to an output folder. Supports GPU acceleration when available.

------------------------------------------------------------------------

## Features

-   Automatic transcription using Whisper
-   Real-time monitoring of an input folder
-   Converts MP3, WAV, M4A, FLAC, OGG to WAV
-   GPU acceleration (CUDA) if available
-   Minimal Python dependencies
-   Easy setup and usage

------------------------------------------------------------------------

## Installation

Follow the steps below to set up the environment.
### 0. Clone repository
```bash
git clone <url>
cd Whisper-based-Transcriber
```

### 1. Create a Python Virtual Environment

Linux / macOS: 
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell): 
```bash
python -m venv venv
.\venv\Scripts\Activate
```
------------------------------------------------------------------------

## 2. Install Required Packages

Make sure the virtual environment is activated, then run:
```bash
pip install -r requirements.txt
```
------------------------------------------------------------------------

## 3. Install FFmpeg (Required)

Ubuntu: 
```bash
sudo apt install ffmpeg
```

macOS (Homebrew): 
```bash
brew install ffmpeg
```

Windows: 
Download from: https://www.gyan.dev/ffmpeg/builds/ 
Make sure FFmpeg is added to your system PATH.

------------------------------------------------------------------------

## Folder Structure
```
project/
│── transcriber.py
│── requirements.txt
│── README.md
│── inputs/   (place audio files here)
└── outputs/  (transcripts appear here)
```
------------------------------------------------------------------------

## How to Use

1.  Put audio files into the `inputs/` folder.

2. Change the input and output paths in `transcribe.py` to your own paths

2.  Run the transcriber:
```bash
python3 transcribe.py
```

3.  The transcript text files will be saved in the `outputs/` folder.

The script performs: - audio → WAV conversion - Whisper transcription -
automatic text file generation - continual watching of the input folder

------------------------------------------------------------------------


## GPU Support

If PyTorch with CUDA is installed, Whisper will automatically use the
GPU. If CUDA is not available, it will fall back to CPU.

------------------------------------------------------------------------

## License

MIT License. You are free to modify and use this project.

