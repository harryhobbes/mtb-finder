import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
@login_required
def index():
    db = get_db()
    users = db.execute(
        'SELECT u.*'
        ' FROM user u'
        ' ORDER BY u.username ASC'
    ).fetchall()
    return render_template('user/index.html', users=users)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    user = get_user(id)

    if request.method == 'POST':
        slack_api_key = request.form['slack_api_key']

        error = False
        if not slack_api_key:
            error = True
            flash('Slack API Key is required.')

        if not error:
            db = get_db()
            db.execute(
                'UPDATE user SET slack_api_key = ?'
                ' WHERE id = ?',
                (slack_api_key, id)
            )
            db.commit()
            return redirect(url_for('user.index'))

    return render_template('user/update.html', user=user)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_user(id)
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('user.index'))

def get_user(id):
    user = get_db().execute(
        'SELECT u.*'
        ' FROM user u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchone()

    if user is None:
        abort(404, f"User id {id} doesn't exist.")

    return user