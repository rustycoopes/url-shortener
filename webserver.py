
import os
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
from nanoid import generate
from flask import Flask, redirect, url_for, render_template, jsonify, request
app = Flask(__name__)
from invalid_usage import InvalidUsage
from validation import validate_shortener_request
from datastore import MappingCollection
from configparser import ConfigParser


@app.route('/home', methods=['GET'])
def view_home():
    return render_template('index.html', content='')


@app.route('/mappings', methods=['GET'])
def view_mappings():
    global mappings
    _all = mappings.load_all()
    return render_template('view.html', content=_all)

@app.route('/mapping/<slug>', methods=['GET'])
def view(slug=''):
    logging.info('slug received {}'.format(slug))
    global mappings
    _mapping = mappings.load_mapping(slug)
    return render_template('add.html', slug=_mapping['slug'], url=_mapping['url'])

@app.route('/<slug>', methods=['GET'])
def serve(slug):
    """
    provides the redirection of the http request to a mapped URL
    OR, provides a json error message if no mapping exists
    Slug =  None, we will never see a call go into this method as it will fall into the velow.
    """
    if slug == 'favicon.ico':
        return ''

    logging.info('slug received \'{}\', loading mapping'.format(slug))
    global mappings
    _mapping = mappings.load_mapping(slug)

    if _mapping:
        return redirect(_mapping['url'])
    else: 
        logging.warning('slug received {}, mapping could not be found.'.format(slug))
        return jsonify({'error':'mapping not found, url to redirect could not be performed.'})
 


@app.route('/', methods=['GET', 'POST'])
def serve_or_save():
    """
    This method will be called to save a mapping or redirect based on a json request, as opposed to in the rest uri
    If just slug provided, a mapping lookup and redirect will be attempted.
    If a url is provided and a slug isnt, then a slug is generated.  The mapping is saved, and the mapping is returned.
    if both slug and url are provided then we just redirect to the url
    Otherwise - error on validation check (we need on or other)
    """
    _errors = validate_shortener_request(request)
    # TODO : every call in seems to make three calls of this method (could be linked to call for favicon.ico)
    
    if _errors is not None: # we must have atleast a URL or a slug
        logging.warning('invalid json submission, redirecting to root page')
        return render_template('index.html', content='')

    _slug = request.json.get('slug', None)
    _url = request.json.get('url', None)

    if _both_url_and_slug_provided(_slug , _url): # We have been provided both, just redirect
        logging.info('saving provided slug "{}" and url "{}" will then redirect to url'.format(_slug, _url))
        return redirect(_url)

    elif _just_url_provided(_slug, _url): # if providing a url, we need to create and store new slug
        logging.info('saving NEW slug "{}" and url "{}" will then redirect to url'.format(_slug, _url))
        _slug, _errors = _generate_slug_and_save(_url)
        return jsonify({'slug': _slug, 'url':_url,'errors':_errors})

    elif _just_slug_provided(_slug, _url):  
        return serve(_slug)

def _generate_slug_and_save(url):
        _slug = generate('1234567890abcdef', 5)  
        _errors = ''
        global mappings
        if not mappings.save_mapping(_slug, url):
            _errors = 'Failed to save'
            logging.warning('failed to save document {}'.format(_errors))
        return (_slug, _errors)

def _both_url_and_slug_provided(slug, url):
    return slug is not None and url is not None

def _just_url_provided(slug, url):
    return url is not None and slug is None

def _just_slug_provided(slug, url):
    return slug is not None and url is None

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
   _response = jsonify(error.to_dict())
   _response.status_code = error.status_code
   return _response

def is_development():
    return not 'gunicorn' in os.environ.get('SERVER_SOFTWARE', '')


"""
START OF MAIN RUN SECTION
"""
conf = ConfigParser()  
conf.read(r'./config/production.cfg')
dataStoreConnectionString = conf['datastore']['ConnectionString']
collectionName = conf['datastore']['CollectionName']
databaseName = conf['datastore']['DatabaseName']
mappings = MappingCollection(dataStoreConnectionString, databaseName, collectionName)

if __name__ == '__main__':
    if is_development():
        app.run(debug=True)

