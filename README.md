# SimplePyWhisperFFMPEG

## Description
A simple implementation of OpenAI's Whisper in Python with some quality-of-life (QoL) functions for easier file handling and format support.

## Features
- Choose files using a file dialog.
- MP4/MP4 sequence support with FFMPEG.
- MP3/WAV support.
- Save results by name into different directories.
- Save in txt, tsv, and srt formats.

## Dependencies
- OpenAI Whisper
- easygui
- FFMPEG-python

Any of these dependencies can be installed with pip:

```bash
pip install
```

## Use with GPU
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -U openai-whisper
```

## How to run
```bash
python main.py
```