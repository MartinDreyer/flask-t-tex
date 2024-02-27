from flask import (
    Blueprint, flash, g, render_template, request, url_for, redirect
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import io
import traceback
from t_tex.auth import login_required
from t_tex.db import get_db
from t_tex.process import (allowed_file, transcribe_file, optimize_file, delete_file, delete_output, get_transcription)
bp = Blueprint('upload_form', __name__)
transcriptions_bp = Blueprint('transcriptions', __name__)

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
                    # Create directory for uploads, if it doesn't exist.
                    upload_dir = os.path.abspath(os.path.join(os.getcwd(), 'uploads/'))
                    os.makedirs(upload_dir, exist_ok=True)

                    # Save file
                    filename = secure_filename(file.filename)
                    path = os.path.join(upload_dir, filename)
                    file.save(path)

                    # Optimize file with ffmpeg
                    optimize_file(path)

                    # Delete original uploaded file.
                    delete_file(path)

                    # Set path for optimized file
                    ogg_file = path.split(".")[0] + ".ogg"

                    # Create output directory if it doesn't exist
                    output_dir = os.path.join(os.getcwd(), 'output/')
                    os.makedirs(output_dir, exist_ok=True)

                    # Transcribe file
                    transcription = transcribe_file(ogg_file)

                    if transcription:
                        base = Path(os.path.join(upload_dir, filename)).stem
                        output_path = os.path.join(output_dir, (base + '.srt'))

                        # Save SRT to database
                        db = get_db()
                        with open(output_path, "r") as f:
                            body = f.read()
                        db.execute(
                            'INSERT INTO transcription (title, body, author_id)'
                            ' VALUES (?, ?, ?)',
                            (base, body, g.user['id'])
                        )
                        db.commit()

                    # Delete SRT and ogg-file locally
                    try:
                        delete_file(ogg_file)
                        delete_output(path)
                    except:
                        pass

                    # Redirect user to transcriptions on success
                    return redirect(url_for('transcriptions.index'))
                                      
                except Exception as e:
                    traceback.print_exc()
                    flash('An error occurred while processing the file')
                    return render_template('upload_form/error.html', error=str(e))

            else:
                flash(f'Invalid file format for {key}')
                return render_template('upload_form/error.html', error=f"Ugyldig filformat for {key}")


    except Exception as e:
        traceback.print_exc()
        flash(f'An error occurred: {str(e)}')
        return render_template('upload_form/error.html', error=str(e))
