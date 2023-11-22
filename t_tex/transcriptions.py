from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from t_tex.auth import login_required
from t_tex.db import get_db


bp = Blueprint('transcriptions', __name__)


@bp.route('/', methods=['GET'])
@login_required
def index():
    db = get_db()
    transcriptions = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM transcription p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()


    return render_template('transcriptions/index.html', transcriptions=transcriptions)



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        error = None        

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO transcription (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('transcriptions.index'))

    return render_template('transcriptions/create.html')

def get_transcription(id, check_author=True):
    transcription = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM transcription p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if transcription is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and transcription['author_id'] != g.user['id']:
        abort(403)

    return transcription

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    transcription = get_transcription(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE transcription SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('transcriptions.index'))

    return render_template('transcriptions/update.html', transcription=transcription)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_transcription(id)
    db = get_db()
    db.execute('DELETE FROM transcription WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('transcriptions.index'))