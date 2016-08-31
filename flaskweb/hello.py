#!/usr/bin/env python
# -*- coding=utf-8 -*-


from flask import Flask, request, render_template
from flask.ext.script import Manager, Bootstrap


#  app = Flask(__name__)
#  manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    #  user_agent = request.headers.get('User_Agent')
    #  return '<h2>Welcome to Flask!</h2>'
    #  return '<p> Your brower is {0}</p>'.format(user_agent)
    #  return '<p> {0} </p>'.format(dir(request)), 200
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    #  return '<h1>Hello, {0}!<h1>'.format(name.encode('utf-8'))
    d = {'name': name, 'age': 26}
    lst = ['&', '<h1>tab</h1>', 'tanggu']
    #  lst = '<h1>tab</h1>'
    return render_template('user.html', datas=d, lst=lst)

@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

if __name__ == '__main__':
    #  app.run(debug=True)
    #  manager.run()
    bootstrap.run()
