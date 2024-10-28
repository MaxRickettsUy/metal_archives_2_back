from flask import (
    Blueprint, flash, g, redirect, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('band', __name__, url_prefix='/band')

#this needs to be paginated
@bp.route('/')
def get_all_bands():
    db = get_db()
    bands = db.execute(
        'SELECT * FROM band'
    ).fetchall()
    return bands

@bp.route('/create', methods=('POST'))
@login_required
def create():
    name = request.form['name']
    error = None

    if not name:
        error = 'Name is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO band (name) VALUES (?)',
            (name)
        )
        db.commit()
        return {"status": "good job"}
        #return redirect(url_for('index'))

#seems like this should include the releases (id, year, name) + avg(review score) count(reviews) 
@bp.route('/<int:id>', methods=('GET'))
def get_one_band(id):
    band = get_band(id)
    return band

def get_band(id):
    band = get_db().execute(
        'SELECT * FROM band WHERE id = ?',
        (id,)
    ).fetchone()

    if band is None:
        abort(404, f"Band id {id} doesn't exist.")
    
    return band

@bp.route('/<int:id>/update', methods=('POST'))
@login_required
def update(id):
    band = get_band(id)

    #build out as band object expands
    #has to be a better way to do this to be more dynamic
    name = request.form['name']
    error = None

    if not name:
        error = 'Name is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'UPDATE band SET name = ? WHERE id = ?',
            (name, id)
        )
        db.commit()
        return {"status": "good job"}
        #return redirect(url_for('index'))


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_band(id)
    db = get_db()
    db.execute('DELETE FROM band WHERE id = ?', (id,))
    db.commit()
    return {"status": "good job"}
    #return redirect(for_url('index'))
