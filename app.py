"""

RANDOM BIRB SITE.

:copyright: (c) 2017 Jakeoid.
:license: MIT, see LICENSE.md for details.

"""

# KYOUKAI
from kyoukai import Kyoukai
from kyoukai import util
# RANDOM
from random import randint
# OS
from os import walk, path
# JSON
import json

# ############################

app = Kyoukai(__name__)

# Storing our files.
global files

# Make our files an empty list.
files = []

# Run through all the files in the img folder.
for (dirpath, dirnames, filenames) in walk('img/'):
    # Get all the filenames
    files.extend(filenames)
    # Beep
    break

# ############################


# Site Index.
@app.route("/")
async def index(ctx):
    """Display the homepage of the website."""
    with open("templates/index.html") as file:
        return util.as_html(file.read())


# Text API Endpoint.
@app.route('/tweet/')
async def tweet(ctx):
    """Host the API in which you can get random birbs from."""
    url = randint(0, len(files) - 1)
    return util.as_html("%s" % files[url])


# JSON API Endpoint.
@app.route('/tweet.json/')
async def tweetjson(ctx):
    """Host the API in which you can get random birbs from."""
    url = randint(0, len(files) - 1)
    return json.dumps({'file': files[url]})


# Text API Endpoint.
@app.route('/tweet/random')
async def tweetrandom(ctx):
    """Host the API in which you can get random birbs from."""
    url = randint(0, len(files) - 1)
    return util.as_html('<meta http-equiv="refresh" content="0 url=http://birb.pw/img/%s" />' % files[url])


# Image Hoster.
@app.route('/img/<filename>')
async def image(ctx, filename):
    """Serve the images of the /img/ and other folders."""
    location = 'img/' + filename

    with open(location, mode='rb') as file:
        stream = file.read()

    return stream


# ############################

# Run our App.
app.run(ip="127.0.0.1", port=5000)
