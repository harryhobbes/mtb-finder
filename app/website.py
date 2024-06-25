import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('website', __name__, url_prefix='/website')

@bp.route('/')
@login_required
def index():
    db = get_db()
    websites = db.execute(
        'SELECT u.*'
        ' FROM website u'
        ' ORDER BY u.title ASC'
    ).fetchall()
    return render_template('website/index.html', websites=websites)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    website = get_website(id)

    if request.method == 'POST':
        slack_api_key = request.form['slack_api_key']

        error = False
        if not slack_api_key:
            error = True
            flash('Slack API Key is required.')

        if not error:
            db = get_db()
            db.execute(
                'UPDATE website SET slack_api_key = ?'
                ' WHERE id = ?',
                (slack_api_key, id)
            )
            db.commit()
            return redirect(url_for('website.index'))

    return render_template('website/update.html', website=website)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_website(id)
    db = get_db()
    db.execute('DELETE FROM website WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('website.index'))

def get_website(id):
    website = get_db().execute(
        'SELECT u.*'
        ' FROM website u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchone()

    if website is None:
        abort(404, f"website id {id} doesn't exist.")

    return website