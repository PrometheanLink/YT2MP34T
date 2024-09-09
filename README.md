# YT2MP34T
YT2MP34T: Video Downloader and Whisper Transcriber

YT2MP34T is a user-friendly application that downloads audio from popular video site, converts them to MP3, and optionally transcribes the audio using OpenAI's Whisper model. This app is designed to provide a simple yet powerful solution for extracting audio and generating transcriptions locally on your machine, without requiring cloud credits or tokens.
Features:

    Download video audio as MP3 from a popular video site
    Transcribe audio using Whisper with GPU acceleration (if available)
    Select from multiple transcription formats: MP3, text, or Whisper transcription
    Real-time progress tracking with a built-in timer for the transcription process
    Clean and organized UI for ease of use
    Detailed logging for troubleshooting and performance monitoring

Prerequisites:

    Python 3.10 or later
    FFmpeg installed and available in your system's PATH (for MP3 conversion)
    NVIDIA GPU with CUDA support (optional, for GPU acceleration with Whisper)

Setup

    Clone the repository:

    bash

git clone https://github.com/your-username/YT2MP34T.git
cd YT2MP34T

Create and activate a Python virtual environment:

bash

python -m venv yt2mp34t_env
source yt2mp34t_env/bin/activate  # On Windows, use `yt2mp34t_env\Scripts\activate`

Install the required dependencies:

bash

    pip install -r requirements.txt

    Ensure FFmpeg is installed and accessible via your system PATH.

Usage

    Run the main application:

    bash

    python yt2mp34t.py

    Enter the video URL in the provided input field.

    Select the desired output format:
        MP4: Download the video in MP4 format.
        MP3: Download and convert the video to MP3.
        Text: Extract captions (if available).
        Whisper Transcription: Transcribe audio using OpenAI’s Whisper model.

    Monitor the real-time progress via the progress bar, and view the timer for MP3 conversion/transcription duration.

    After the process completes, the files will be saved in your chosen output folder.

Output

    MP3: The audio file will be saved as video_title.mp3 in the selected output directory.
    Whisper Transcription: The transcription will be saved as video_title_transcription_whisper.txt.
    Text: Caption-based transcripts will be saved as .txt files in the output folder.

GPU Acceleration

If you have an NVIDIA GPU with CUDA support, Whisper will automatically use it to speed up the transcription process. Make sure you have the CUDA toolkit and a GPU-enabled PyTorch installed.
Notes

    FFmpeg is required for MP3 conversion, and it must be accessible via your system PATH.
    Larger Whisper models (e.g., "large") may require more computational resources and will take longer to transcribe, especially without GPU acceleration.

Troubleshooting

    FFmpeg Issues: Ensure FFmpeg is installed correctly and accessible in your system PATH.
    Dependency Issues: Reinstall the required packages with pip install -r requirements.txt or manually install any missing dependencies.
    Download Failures: Verify if yt-dlp supports the video platform, and ensure the video is still available.
    Check the log file transcription_debug.log for detailed error information.

Contributing

Feel free to fork this repository and submit pull requests with any enhancements or bug fixes.
License

This project is licensed under the MIT License:

MIT License

Copyright (c) 2024 PrometheanLink LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
