# -*- coding: utf-8 -*-
# ┌┐ ┬┬─┐┌┐
# ├┴┐│├┬┘├┴┐
# └─┘┴┴└─└─┘
#
# RANDOM BIRB SITE
# :copyright: (c) 2017 Jakeoid
# :license: MIT, see LICENSE.md for details.

# FLASK
from flask import Flask, jsonify, render_template, send_from_directory
# RANDOM
from random import randint
# OS
from os import walk

# ############################

# Flask APP
app = Flask(__name__)

# Storing our files.
global f

# Make our files an empty list.
f = []

# Run through all the files in the img folder.
for (dirpath, dirnames, filenames) in walk('img/'):
    # Get all the filenames
    f.extend(filenames)
    # Beep
    break

# ############################


# Image Hoster.
@app.route('/img/<path:filename>')
def image(filename):
    """ Serves the images of the /img/ and other folders """
    return send_from_directory('./img/', filename)


# Site Index.
@app.route('/')
def index():
    """ Hosts the homepage of the website (API DOCUMENTATION) """
    return render_template('index.html')


# API Endpoint.
@app.route('/tweet', methods=['GET'])
def tweet():
    """ Hosts the API in which you can get random birbs from. """
    url = randint(0, len(f) - 1)
    return jsonify({'file': f[url]})

# ############################

if __name__ == '__main__':
    app.run()
