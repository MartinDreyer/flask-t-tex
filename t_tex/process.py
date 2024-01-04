import os
import whisper
import traceback
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
        command = '-i ' + filename + ' -vn -map_metadata -1 -ac 1 -c:a libopus -b:a 12k -application voip ' + filename.split(".")[0] + '.ogg'
        ffmpeg_path = "ffmpeg" # In windows place ffmpeg.exe in t_tex: os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
        cmd_string = ffmpeg_path + ' ' + command
        subprocess.call(cmd_string, shell=True)
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
        subprocess.run(['whisper', filename, '--language', language, '--model', model_name, '--output_dir', OUTPUT_DIR], capture_output=True)
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

# @profile
# def float_to_time(float_value: float):
#     milliseconds = int((float_value % 1) * 1000)
#     seconds = int(float_value % 60)
#     minutes = int((float_value // 60) % 60)
#     hours = int(float_value // 3600)

#     time_str = f'{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}'
#     return time_str

# @profile
# def output_to_text_file(data_dict: dict, output_file_name: str):
#     index = 1
#     try:
#         with open(output_file_name, 'w', encoding='utf-8') as file:
#             for value in data_dict['segments']:
#                 start_time_str = float_to_time(value['start'])
#                 end_time_str = float_to_time(value['end'])
#                 text = value['text'].strip()
#                 file.write(f'{index}\n')
#                 file.write(f'{start_time_str} --> {end_time_str}\n')
#                 file.write(f'{text}\n\n')
#                 index += 1
#             file.close()

#     except Exception as e:
#         print(f'Fejl ved skrivning til tekstfil: {e}')