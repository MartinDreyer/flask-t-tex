from flask import (
    Blueprint, flash, render_template, request, send_from_directory
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import io
import traceback
from t_tex.auth import login_required
from t_tex.db import get_db
from t_tex.process import (allowed_file, transcribe, output_to_text_file)
bp = Blueprint('upload_form', __name__)

ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'wav', 'avi'}


@bp.route('/upload_form', methods=['GET'])
@login_required
def upload_form():
    return render_template('upload_form/upload_form.html')

@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    try:
        # Check if there are files in the request
        if len(request.files) == 0:
            flash('No files in the request')
            return render_template('upload_form/error.html', error="Ingen filer i forespørselen")


        for key in request.files:
            file = request.files[key]

            if file.filename == '':
                flash(f'No selected file for {key}')
                return render_template('upload_form/error.html', error=f"Ingen fil valgt for {key}")

            if file and allowed_file(file.filename):
                try:
                    upload_dir = os.path.join(os.getcwd(), 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)

                    filename = secure_filename(file.filename)
                    base = Path(os.path.join(upload_dir, filename)).stem

                    filepath = os.path.join(upload_dir, filename)
                    file.save(filepath)

                    transcription = transcribe(filepath, language='danish', model_size='large')
                    
                    if transcription:
                        srt_dir = os.path.join(os.getcwd(), 'srt')
                        os.makedirs(srt_dir, exist_ok=True)
                        output_to_text_file(transcription, os.path.join(srt_dir, (base + '.srt')))

                                           

                except Exception as e:
                    traceback.print_exc()
                    flash('An error occurred while processing the file')
                    return render_template('upload_form/error.html', error=str(e))

            else:
                flash(f'Invalid file format for {key}')
                return render_template('upload_form/error.html', error=f"Ugyldig filformat for {key}")

        return "Files successfully uploaded!"

    except Exception as e:
        traceback.print_exc()
        flash(f'An error occurred: {str(e)}')
        return render_template('upload_form/error.html', error=str(e))
