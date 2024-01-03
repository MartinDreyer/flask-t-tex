import os
import whisper
import traceback
import torch
import subprocess

ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'wav', 'avi'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def optimize_file(filename):
    command = '-i ' + filename + ' -vn -map_metadata -1 -ac 1 -c:a libopus -b:a 12k -application voip ' + filename.split(".")[0] + '.ogg'
    ffmpeg_path = "ffmpeg" # In windows place ffmpeg.exe in t_tex: os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
    cmd_string = ffmpeg_path + ' ' + command
    subprocess.call(cmd_string, shell=True)
    
def delete_file(filename):
    os.remove(filename)

def transcribe_file(filename):
    model = whisper.load_model("large")
    audio = whisper.load_audio(filename)
    transcription = model.transcribe(audio=audio, verbose=True, fp16=False, word_timestamps=True, language="danish")
    return transcription


def float_to_time(float_value: float):
    milliseconds = int((float_value % 1) * 1000)
    seconds = int(float_value % 60)
    minutes = int((float_value // 60) % 60)
    hours = int(float_value // 3600)

    time_str = f'{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}'
    return time_str

def output_to_text_file(data_dict: dict, output_file_name: str):
    index = 1
    try:
        with open(output_file_name, 'w', encoding='utf-8') as file:
            for value in data_dict['segments']:
                start_time_str = float_to_time(value['start'])
                end_time_str = float_to_time(value['end'])
                text = value['text'].strip()
                file.write(f'{index}\n')
                file.write(f'{start_time_str} --> {end_time_str}\n')
                file.write(f'{text}\n\n')
                index += 1
            file.close()

    except Exception as e:
        print(f'Fejl ved skrivning til tekstfil: {e}')