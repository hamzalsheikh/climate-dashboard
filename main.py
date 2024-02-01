import os
from time import sleep, time
from flask import Flask, render_template, url_for, stream_with_context, request, Response, flash
from pygtail import Pygtail

app = Flask(__name__)


# INDEX 
@app.route('/')
def dirtree():
    path = os.path.expanduser(u'static')
    return render_template('index.html', tree=make_tree(path))

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree

# IMAGES
@app.route('/<image>')
def display_image(image):
    path = os.path.expanduser(u'static/images')
    img = find(image, 'static/images/pythonprd')
    print(image)
    return render_template('index.html', tree=make_tree(path), image=img)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


# LOGS
@app.route('/logs')
def display_log():
    path = os.path.expanduser(u'static/logs')
    #log = find(log, 'static/logs')
    #print(log)
    return render_template('log.html', tree=make_tree(path))


@app.route('/logging-loop/<logFile>')
def stream(logFile):
    def generate():
        with open("static/logs/" + logFile) as f:
            while True:
                yield f.read()
                sleep(1)

    return app.response_class(generate(), mimetype='text/plain') # render_template('logging.html', logs=generate())

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8888, debug=True) 