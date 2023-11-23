import os
import whisper
import traceback
import torch

ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'wav', 'avi'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def transcribe(filename: str, language: str = 'danish', model_size: str = 'large'):
    try:
        print('Indlæser transskriberingsmodel.')
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        
        if torch.cuda.is_available():
            print("Running on GPU - cuda is available")
        else:
            print("Running on CPU - cuda is NOT available")
        
        model = whisper.load_model(model_size, device=DEVICE)
        
        if model is None:
            print("Failed to load the transcribing model.")
            return None

        print(f'Transskriberingsmodel indlæst.')
        print(f'Transskriberer fil: {filename}')
        
        transcription = model.transcribe(
            filename,
            language=language,
            fp16=False,
            verbose=True,
            word_timestamps=True
        )

        if transcription:
            print('Transskribering færdig.')
        
        return transcription
    except Exception as e:
        traceback.print_exc()
        print(f'Fejl under transskribering: {e}')
        return None


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