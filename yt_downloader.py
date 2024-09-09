import os
import time
from pytubefix import YouTube
from pytubefix.cli import on_progress
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from urllib.parse import urlparse, parse_qs
from moviepy.editor import AudioFileClip  # For MP3 conversion
import pytube  # For caption extraction
import torch
import whisper
import threading

def clean_url(url):
    if 'youtube' in url or 'youtu.be' in url:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if parsed_url.netloc == 'youtu.be':
            video_id = parsed_url.path.lstrip('/')
            return f"https://www.youtube.com/watch?v={video_id}"
        if 'v' in query_params:
            return f"https://www.youtube.com/watch?v={query_params['v'][0]}"
    return url

def on_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_var.set(percentage_of_completion)
    progress_bar.update()

def download_video(video_url, save_path, file_format):
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress_callback)
        print(f"Title: {yt.title}")
        print(f"Length: {yt.length} seconds")

        if file_format == 'mp4':
            video_stream = yt.streams.get_highest_resolution()
            if video_stream is None:
                print("The highest resolution stream is not available.")
                return
            video_stream.download(output_path=save_path)
            print(f"Download completed and saved to {save_path}")

        elif file_format == 'mp3':
            start_timer()  # Start the timer before MP3 conversion
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream is None:
                print("Audio stream is not available.")
                return
            audio_path = audio_stream.download(output_path=save_path)
            mp3_path = os.path.splitext(audio_path)[0] + '.mp3'
            AudioFileClip(audio_path).write_audiofile(mp3_path)
            os.remove(audio_path)  # Remove the original downloaded file
            print(f"MP3 conversion completed and saved to {mp3_path}")
            stop_timer()  # Stop the timer after MP3 conversion

        elif file_format == 'text':
            caption = yt.captions.get_by_language_code('en')
            if caption is None:
                print("No English captions available.")
                return
            text_path = os.path.join(save_path, f"{yt.title}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(caption.generate_srt_captions())
            print(f"Text extraction completed and saved to {text_path}")

        elif file_format == 'whisper':
            start_timer()  # Start the timer for Whisper transcription
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream is None:
                print("Audio stream is not available.")
                return
            audio_path = audio_stream.download(output_path=save_path)
            mp3_path = os.path.splitext(audio_path)[0] + '.mp3'
            AudioFileClip(audio_path).write_audiofile(mp3_path)
            os.remove(audio_path)  # Remove the original downloaded file
            print(f"MP3 conversion completed and saved to {mp3_path}")
            
            # Call Whisper for transcription
            transcribe_with_whisper(mp3_path, save_path)
            stop_timer()  # Stop the timer after transcription

        # Show a dialog to open the file location
        if messagebox.askyesno("Open Folder", "Download complete. Do you want to open the folder?"):
            os.startfile(save_path)
        
    except Exception as e:
        print(f"An error occurred: {e}")

def transcribe_with_whisper(mp3_file, save_path):
    try:
        # Load the Whisper model (choose from tiny, base, small, medium, large)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("base", device=device)

        print(f"Using Whisper model on device: {device}")
        print(f"Transcribing file: {mp3_file}")

        # Transcribe the audio file
        result = model.transcribe(mp3_file)

        # Save transcription to a file
        output_file = os.path.join(save_path, f"{os.path.basename(mp3_file).replace('.mp3', '')}_transcription_whisper.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result['text'])

        print(f"Transcription completed and saved to {output_file}")

    except Exception as e:
        print(f"An error occurred during Whisper transcription: {e}")

def get_save_path():
    save_path = filedialog.askdirectory(title="Select Download Folder")
    return save_path

def start_download():
    video_url = url_entry.get()
    clean_video_url = clean_url(video_url)
    print(f"Cleaned URL: {clean_video_url}")
    save_path = get_save_path()
    if save_path:
        download_thread = threading.Thread(target=download_video, args=(clean_video_url, save_path, format_var.get()))
        download_thread.start()  # Start the download in a separate thread to keep the GUI responsive

def start_timer():
    global start_time
    start_time = time.time()
    update_timer()

def stop_timer():
    global running_timer
    running_timer = False

def update_timer():
    global running_timer
    running_timer = True
    def count():
        while running_timer:
            elapsed_time = time.time() - start_time
            minutes, seconds = divmod(elapsed_time, 60)
            timer_label.config(text=f"Time: {int(minutes):02}:{int(seconds):02}")
            time.sleep(1)
    timer_thread = threading.Thread(target=count)
    timer_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("YouTube Video Downloader with Whisper Transcription")

    # Padding around all elements
    padding_options = {'padx': 10, 'pady': 10}

    # Frame for URL input
    url_frame = tk.LabelFrame(root, text="YouTube Video URL", padx=10, pady=10)
    url_frame.pack(fill="both", padx=10, pady=10)
    tk.Label(url_frame, text="Enter the YouTube video URL:").pack(anchor=tk.W)
    url_entry = tk.Entry(url_frame, width=50)
    url_entry.pack(anchor=tk.W)

    # Frame for format selection
    format_frame = tk.LabelFrame(root, text="Select Format", padx=10, pady=10)
    format_frame.pack(fill="both", padx=10, pady=10)
    format_var = tk.StringVar(value='mp4')  # Default to MP4
    tk.Radiobutton(format_frame, text="MP4", variable=format_var, value='mp4').pack(side=tk.LEFT, padx=10)
    tk.Radiobutton(format_frame, text="MP3", variable=format_var, value='mp3').pack(side=tk.LEFT, padx=10)
    tk.Radiobutton(format_frame, text="Text", variable=format_var, value='text').pack(side=tk.LEFT, padx=10)
    tk.Radiobutton(format_frame, text="Whisper Transcription", variable=format_var, value='whisper').pack(side=tk.LEFT, padx=10)

    # Frame for progress and timer
    progress_frame = tk.LabelFrame(root, text="Progress", padx=10, pady=10)
    progress_frame.pack(fill="both", padx=10, pady=10)
    
    # Progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
    progress_bar.pack(pady=10, fill=tk.X, padx=10)

    # Timer label
    timer_label = tk.Label(progress_frame, text="Time: 00:00")
    timer_label.pack()

    # Download button
    download_button = tk.Button(root, text="Download", command=start_download)
    download_button.pack(pady=20)

    root.mainloop()

