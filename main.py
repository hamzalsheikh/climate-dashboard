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


import os
from flask import Flask, render_template, url_for


app = Flask(__name__)

@app.route('/')
def dirtree():
    path = os.path.expanduser(u'static')
    return render_template('index.html', tree=make_tree(path))

@app.route('/<image>')
def display_image(image):
    path = os.path.expanduser(u'static')
    img = find(image, 'static')
    print(image)
    return render_template('index.html', tree=make_tree(path), image=img)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

if __name__=="__main__":
    app.run(host='localhost', port=8888, debug=True)