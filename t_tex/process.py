import os
import torch
import subprocess
from memory_profiler import profile
from pathlib import Path
import glob



ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'wav', 'avi'}
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
OUTPUT_DIR = os.path.join(os.getcwd(), 'output/')
MAX_LINE_COUNT = 42
THREADS = 4
WORD_TIMESTAMPS = True
model_name = "large-v3"
language="da"

@profile
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile
def optimize_file(filename):
    try:
        print("Converting file to .ogg")
        output_filename = filename.split(".")[0] + '.ogg'

        ffmpeg_path = "ffmpeg"  # In Windows, provide the full path to ffmpeg.exe if not in the system PATH

        # Construct the command as a list of arguments
        command = [
            ffmpeg_path,
            '-i', filename,
            '-vn',
            '-map_metadata', '-1',
            '-ac', '1',
            '-c:a', 'libopus',
            '-b:a', '12k',
            '-application', 'voip',
            output_filename
        ]

        # Run the command using subprocess.run()
        result = subprocess.run(command, shell=False)

        # Check the return code
        if result.returncode == 0:
            print(f"Conversion successful. Output file: {output_filename}")
        else:
            print(f"Error during conversion. Return code: {result.returncode}")
            print(result.stderr)
    except Exception as e:
        print(f"Error: {e}")
    
@profile
def delete_file(filename):
    try:
        print(f"Deleting file: {filename}")
        os.remove(filename)
    except Exception as e:
        print(f"Error: {e}")

@profile
def get_transcription(filename, extension):
    try: 
        print("Getting transcription")
        stem = Path(filename).stem
        path = os.path.join(OUTPUT_DIR, stem)
        with open(path + extension, "r") as f:
            transcription = f.read()
    except Exception as e:
        print(f"Error: {e}")
    return transcription

@profile
def transcribe_file(filename):
    try:
        command = [
            'whisper', 
            filename,
            '--language', 
            language, 
            '--model', 
            model_name, 
            '--output_dir', 
            OUTPUT_DIR, 
            '--device', 
            DEVICE]
        
        result = subprocess.run(
            command, 
            capture_output=True,
            shell=False)
        
        # Check the return code
        if result.returncode == 0:
            print(f"Transcription successful.")
        else:
            print(f"Error during transcription. Return code: {result.returncode}")
            print(result.stderr)

        transcription = get_transcription(filename, ".json")
    except Exception as e:
        print(f"Error: {e}")
    return transcription



@profile
def delete_output(filename):
    try:
        print(f"Deleting temporary output from: {filename}")
        stem = Path(filename).stem
        file_pattern = os.path.join(OUTPUT_DIR, (stem + ".*"))
        files_to_delete = glob.glob(file_pattern)

            # Iterate through the list and delete each file
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    except Exception as e:
        print(f"Error: {e}")