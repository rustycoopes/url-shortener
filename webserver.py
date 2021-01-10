
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

@app.route('/home', methods=['GET'])
def view_home():
    return render_template('index.html', content='')


@app.route('/mappings', methods=['GET'])
def view_mappings():
    _all = MappingCollection().load_all()
    return render_template('view.html', content=_all)

@app.route('/mapping/<slug>', methods=['GET'])
def view(slug=''):
    logging.info('slug received {}'.format(slug))
    _mapping = MappingCollection().load_mapping(slug)
    return render_template('add.html', slug=_mapping['slug'], url=_mapping['url'])

@app.route('/<slug>', methods=['GET'])
def serve(slug):
    """
    Slug =  None will never go into this method as it will fall into the velow.
    """
    if slug == 'favicon.ico':
        return ''

    if slug is not None:
        logging.info('slug received \'{}\', loading mapping'.format(slug))
        _mapping = MappingCollection().load_mapping(slug)
        if _mapping:
            return redirect(_mapping['url'])
        else: 
            logging.warning('slug received {}, mapping could not be found.'.format(slug))
            return jsonify({'error':'mapping not found, url to redirect could not be performed.'})
 


@app.route('/', methods=['GET', 'POST'])
def serve_or_save():
    
    _errors = validate_shortener_request(request)
    # TODO : every call in seems to make three calls of this method (could be linked to call for favicon.ico)
    
    if _errors is not None: # we must have atleast a URL or a slug
        logging.warning('invalid json submission, redirecting to root page')
        return render_template('index.html', content='')

    _slug = request.json.get('slug', None)
    _url = request.json.get('url', None)

    if _slug is not None and _url is not None: # We have been provided both, just redirect
        logging.info('saving provided slug "{}" and url "{}" will then redirect to url'.format(_slug, _url))
        return redirect(_url)

    elif _url is not None and _slug is None: # if providing a url, we need to create and store new slug
        _slug = generate('1234567890abcdef', 5)  
        logging.info('saving NEW slug "{}" and url "{}" will then redirect to url'.format(_slug, _url))
        _errors = ''
        if not MappingCollection().save_mapping(_slug, _url):
            _errors = 'Failed to save'
            logging.warning('failed to save document {}'.format(_errors))
        return jsonify({'slug': _slug, 'url':_url,'errors':_errors})

    elif _slug is not None and _url is None:
        return serve(_slug)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
   _response = jsonify(error.to_dict())
   _response.status_code = error.status_code
   return _response

def is_development():
    return not 'gunicorn' in os.environ.get('SERVER_SOFTWARE', '')

if __name__ == '__main__':
    if is_development():
        app.run(debug=True)

