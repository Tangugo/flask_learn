#!/usr/bin/env python
# -*- coding=utf-8 -*-


from datetime import datetime

from flask import Flask, request, render_template, url_for, session, redirect, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)
#  moment = Moment(app)


class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    #  user_agent = request.headers.get('User_Agent')
    #  return '<h2>Welcome to Flask!</h2>'
    #  return '<p> Your brower is {0}</p>'.format(user_agent)
    #  return '<p> {0} </p>'.format(dir(request)), 200
    #  return render_template('index.html')
    #  name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
        #  name = form.name.data
        #  form.name.data = ''
    return render_template('index.html', form=form, name=session.get('name'))


app.add_url_rule('/index', endpoint='hello', view_func=index)

@app.route('/user/<name>')
def user(name):
    #  return '<h1>Hello, {0}!<h1>'.format(name.encode('utf-8'))
    d = {'name': name, 'age': 26}
    lst = ['&', '<h1>tab</h1>', 'tanggu']
    #  lst = '<h1>tab</h1>'
    #  return render_template('user.html', name=name)
    return url_for('user', name='tab', _external=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

if __name__ == '__main__':
    app.run(debug=True)
    #  manager.run()
