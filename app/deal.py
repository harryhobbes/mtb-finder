from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

from app.finder import find_deal, get_clean_price
from app.graph import generate_history_graph, generate_test_graph

bp = Blueprint('deal', __name__, url_prefix='/deal')

@bp.app_template_filter()
def format_currency(price):
    return f"${float(price):,.2f}"

@bp.route('/')
def index():
    db = get_db()
    deals = db.execute(
        'SELECT d.id, user_id, title, target_url, css_selector, latest_deal_text, d.created, u.username'
        ' FROM deal d JOIN user u ON d.user_id = u.id'
        ' ORDER BY d.title ASC'
    ).fetchall()
    return render_template('deal/index.html', deals=deals)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        target_url = request.form['target_url']
        css_selector = request.form['css_selector']
        
        error = False
        if not title:
            error = True
            flash('Title is required.')
        
        if not target_url:
            error = True
            flash('Target URL is required.')

        if not css_selector:
            error = True
            flash('CSS Selector is required.')

        if not error:
            db = get_db()
            db.execute(
                'INSERT INTO deal (title, target_url, css_selector, user_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, target_url, css_selector, g.user['id'])
            )
            db.commit()
            return redirect(url_for('deal.index'))

    return render_template('deal/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    deal = get_deal(id)

    if request.method == 'POST':
        title = request.form['title']
        target_url = request.form['target_url']
        css_selector = request.form['css_selector']

        error = False
        if not title:
            error = True
            flash('Title is required.')
        
        if not target_url:
            error = True
            flash('Target URL is required.')

        if not css_selector:
            error = True
            flash('CSS Selector is required.')

        if not error:
            db = get_db()
            db.execute(
                'UPDATE deal SET title = ?, target_url = ?, css_selector = ?'
                ' WHERE id = ?',
                (title, target_url, css_selector, id)
            )
            db.commit()
            return redirect(url_for('deal.index'))

    return render_template('deal/update.html', deal=deal)

@bp.route('/<int:id>/history', methods=('GET',))
def history(id):
    deal = get_deal(id, False)
    deal_history = get_deal_history(id)

    if deal['latest_deal_text'] is None:
        latest_deal_text = '0.00'
    else:
        latest_deal_text = float(deal['latest_deal_text'])

    history_graph = generate_history_graph(deal_history, latest_deal_text)
    
    return render_template('deal/history.html', deal=deal, deal_history=deal_history, history_graph=history_graph)

@bp.route('/refresh')
@login_required
def refresh():
    db = get_db()
    deals = db.execute(
        'SELECT id, title, target_url, css_selector'
        ' FROM deal'
    ).fetchall()

    if deals is None:
        abort(404, "No deals to update")

    for deal in deals:
        price_dirty = find_deal(deal['target_url'], deal['css_selector'])

        if price_dirty:
            update_price_history(deal, price_dirty)

    flash('Refresh complete')

    return redirect('/')

@bp.route('/<int:id>/refreshone', methods=('GET',))
@login_required
def refreshone(id):
    db = get_db()
    deal = get_deal(id)
    if deal is None:
        abort(404, "No deals to update")

    price_dirty = find_deal(deal['target_url'], deal['css_selector'])

    if price_dirty:
        update_price_history(deal, price_dirty)

    flash('Refresh complete')

    return redirect(url_for('deal.history', id=id))

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_deal(id)
    db = get_db()
    db.execute('DELETE FROM deal WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('deal.index'))

def get_deal(id, check_author=True):
    deal = get_db().execute(
        'SELECT d.id, user_id, title, target_url, css_selector, latest_deal_text, d.created, u.username'
        ' FROM deal d JOIN user u ON d.user_id = u.id'
        ' WHERE d.id = ?',
        (id,)
    ).fetchone()

    if deal is None:
        abort(404, f"Deal id {id} doesn't exist.")

    if check_author and deal['user_id'] != g.user['id']:
        abort(403)

    return deal

def get_deal_history(id):
    deal_history = get_db().execute(
        'SELECT created, deal_text'
        ' FROM deal_log'
        ' WHERE deal_id = ?',
        (id,)
    ).fetchall()

    return deal_history

def update_price_history(deal, price_dirty):
    db = get_db()

    price_clean = get_clean_price(price_dirty)

    id = deal['id']
    title = deal['title']

    message = f'{title} current price: {format_currency(price_clean)}'
    print(message)
    send_slack_message(message)
            
    db.execute(
        'INSERT INTO deal_log (deal_id, deal_text)'
        ' VALUES (?, ?)',
        (id, price_clean)
    )
    db.commit()

    db.execute(
        'UPDATE deal SET latest_deal_text = ?'
        ' WHERE id = ?',
        (price_clean, id)
    )
    db.commit()

def send_slack_message(message):
    import os
    from slack_sdk import WebClient
    
    slack_token = os.environ["SLACK_API_KEY"]
    
    client = WebClient(token=slack_token)

    # Send a message
    client.chat_postMessage(
        channel="general", 
        text=message, 
        username="MTB Finder"
    )