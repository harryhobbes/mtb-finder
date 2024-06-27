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
    records = db.execute(
        'SELECT u.*'
        ' FROM website u'
        ' ORDER BY u.title ASC'
    ).fetchall()
    return render_template('website/index.html', records=records)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        base_url = request.form['base_url']
        css_selector = request.form['css_selector']
        
        error = False
        if not title:
            error = True
            flash('Title is required.')
        
        if not base_url:
            error = True
            flash('Base URL is required.')

        if not css_selector:
            error = True
            flash('CSS Selector is required.')

        if not error:
            db = get_db()
            db.execute(
                'INSERT INTO website (title, base_url, css_selector, user_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, base_url, css_selector, g.user['id'])
            )
            db.commit()
            return redirect(url_for('website.index'))

    return render_template('website/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    record = get_record(id)

    if request.method == 'POST':
        title = request.form['title']
        base_url = request.form['base_url']
        css_selector = request.form['css_selector']

        error = False
        if not title:
            error = True
            flash('Title is required.')
        
        if not base_url:
            error = True
            flash('Base URL is required.')

        if not css_selector:
            error = True
            flash('CSS Selector is required.')

        if not error:
            db = get_db()
            db.execute(
                'UPDATE website SET title = ?, base_url = ?, css_selector = ?'
                ' WHERE id = ?',
                (title, base_url, css_selector, id)
            )
            db.commit()
            return redirect(url_for('website.index'))

    return render_template('website/update.html', record=record)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_record(id)
    db = get_db()
    db.execute('DELETE FROM website WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('website.index'))

def get_record(id):
    record = get_db().execute(
        'SELECT w.*'
        ' FROM website w'
        ' WHERE w.id = ?',
        (id,)
    ).fetchone()

    if record is None:
        abort(404, f"Website id {id} doesn't exist.")

    return record