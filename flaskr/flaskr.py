#!/usr/bin/env python
# -*- coding=utf-8 -*-


import os
import sqlite3
from flask import (Flask, request, session, g, redirect, url_for,
                   abort, render_template, flash)

app = Flask(__name__)
app.config.from_object(__name__)

print 'path: ', app.root_path

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = '123'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    #  db = getattr(g, '_databese', None)
    #  if db is None:
    #      db = g._database = sqlite3.connect(DATABASE)
    #  return db
    if not hasattr(g, 'flaskr.db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(exception):
    #  db = getattr(g, '_database', None)
    #  if db is not None:
    #      db.close()
    if hasattr(g, 'flaskr.db'):
        g.sqlite_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def init_db_command():
    init_db()
    print 'Initialized the database.'

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    print db
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            erro = 'Invalid password'
        else:
            session['logged_id'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
