from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from pathlib import Path



from t_tex.auth import login_required
from t_tex.db import get_db


bp = Blueprint('upload_form', __name__)

ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'wav', 'avi'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@bp.route('/upload_form', methods=['GET'])
@login_required
def upload_form():
    return render_template('upload_form/upload_form.html')

@bp.route('/upload', methods=['POST'])
@login_required
def upload():

     if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('error.html', error="Fil mangler")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template('error.html', error="Ingen fil valgt")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            return "hello"