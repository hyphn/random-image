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
# MIMETYPE
import mimetypes

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

settings = None

with open('settings.json') as settingsfile:
    settings = json.load(settingsfile)

# ############################

ip = settings['server']['ip']
port = settings['server']['port']

# ############################


# Site Index.
@app.route("/")
async def index(ctx):
    """Display the homepage of the website."""
    try:
        file_directory = 'templates/' + settings['pages']['index']
    except:
        file_directory = 'templates/index.html'

    with open(file_directory) as file:
        content = file.read()

        content = content.replace(
            '{{AMOUNT}}', str(len(files)))
        content = content.replace(
            '{{NAME}}', settings['meta']['name'])
        content = content.replace(
            '{{DESCRIPTION}}', settings['meta']['description'])
        content = content.replace(
            '{{TYPE}}', settings['meta']['type'])
        content = content.replace(
            '{{TYPE-PLURAL}}', settings['meta']['plural'])
        content = content.replace(
            '{{SITEURL}}', settings['meta']['siteurl'])
        content = content.replace(
            '{{ENDPOINT-MAIN}}', settings['endpoints']['main']['name'])
        content = content.replace(
            '{{ENDPOINT-JSON}}', settings['endpoints']['json']['name'])
        content = content.replace(
            '{{ENDPOINT-RANDOM}}', settings['endpoints']['random']['name'])

        return util.as_html(content)


# Assets Route.
@app.route('/<folder>/<filename>')
async def assets(ctx, folder, filename):
    """Serve the images of the /img/ and other folders."""
    location = folder + '/' + filename

    with open(location, mode='rb') as file:
        stream = file.read()

    header = {
        'Content-Type': mimetypes.guess_type(location)[0]
    }

    return util.Response(stream, status=200, headers=header)


# Text API Endpoint.
@app.route(settings['endpoints']['main']['name'])
async def tweet(ctx):
    """Host the API in which you can get random birbs from."""
    if not settings['endpoints']['main']['enabled']:
        return

    url = randint(0, len(files) - 1)

    header = {
        'Content-Type': 'text/plain'
    }

    return util.as_html("%s" % files[url])


# JSON API Endpoint.
@app.route(settings['endpoints']['json']['name'])
async def tweetjson(ctx):
    """Host the API in which you can get random birbs from."""
    if not settings['endpoints']['json']['enabled']:
        return

    url = randint(0, len(files) - 1)

    header = {
        'Content-Type': 'application/javascript'
    }

    return util.Response(json.dumps({'file': files[url]}), status=200, headers=header)


# Text API Endpoint.
@app.route(settings['endpoints']['random']['name'])
async def tweetrandom(ctx):
    """Host the API in which you can get random birbs from."""
    if not settings['endpoints']['random']['enabled']:
        return

    url = randint(0, len(files) - 1)
    location = 'img/' + files[url]

    with open(location, mode='rb') as file:
        stream = file.read()

    header = {
        'Content-Type': mimetypes.guess_type(location)[0]
    }

    return util.Response(stream, status=200, headers=header)


# Image Hoster.
@app.route('/img/<filename>')
async def image(ctx, filename):
    """Serve the images of the /img/ and other folders."""
    location = 'img/' + filename
    filetype = filename.split('.')[1]

    with open(location, mode='rb') as file:
        stream = file.read()

    header = {
        'Content-Type': 'image/' + filetype
    }

    return util.Response(stream, status=200, headers=header)

# ############################


# Handle 404.
@app.root.errorhandler(404)
async def handle_404(ctx, exc):
    """Serve the 404 (Not Found) Page."""
    try:
        file_directory = 'templates/' + settings['pages']['notfound']
    except:
        file_directory = 'templates/index.html'

    with open(file_directory) as file:
        content = file.read()

        content = content.replace(
            '{{AMOUNT}}', str(len(files)))
        content = content.replace(
            '{{NAME}}', settings['meta']['name'])
        content = content.replace(
            '{{DESCRIPTION}}', settings['meta']['description'])
        content = content.replace(
            '{{TYPE}}', settings['meta']['type'])
        content = content.replace(
            '{{TYPE-PLURAL}}', settings['meta']['plural'])
        content = content.replace(
            '{{SITEURL}}', settings['meta']['siteurl'])
        content = content.replace(
            '{{ENDPOINT-MAIN}}', settings['endpoints']['main']['name'])
        content = content.replace(
            '{{ENDPOINT-JSON}}', settings['endpoints']['json']['name'])
        content = content.replace(
            '{{ENDPOINT-RANDOM}}', settings['endpoints']['random']['name'])

        return util.as_html(content)

# Handle 404.


@app.root.errorhandler(500)
async def handle_500(ctx, exc):
    """Serve the 500 (Server Error) Page."""
    try:
        file_directory = 'templates/' + settings['pages']['servererror']
    except:
        file_directory = 'templates/index.html'

    with open(file_directory) as file:
        content = file.read()

        content = content.replace(
            '{{AMOUNT}}', str(len(files)))
        content = content.replace(
            '{{NAME}}', settings['meta']['name'])
        content = content.replace(
            '{{DESCRIPTION}}', settings['meta']['description'])
        content = content.replace(
            '{{TYPE}}', settings['meta']['type'])
        content = content.replace(
            '{{TYPE-PLURAL}}', settings['meta']['plural'])
        content = content.replace(
            '{{SITEURL}}', settings['meta']['siteurl'])
        content = content.replace(
            '{{ENDPOINT-MAIN}}', settings['endpoints']['main']['name'])
        content = content.replace(
            '{{ENDPOINT-JSON}}', settings['endpoints']['json']['name'])
        content = content.replace(
            '{{ENDPOINT-RANDOM}}', settings['endpoints']['random']['name'])

        return util.as_html(content)

# ############################

# Run our App.
app.run(ip=ip, port=port)
