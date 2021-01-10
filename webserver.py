
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
    # TODO : Make this prettier, and provide adding functionatilty?
    logging.info('slug received {}'.format(slug))
    _mapping = MappingCollection().load_mapping(slug)
    return render_template('add.html', slug=_mapping['slug'], url=_mapping['url'])

@app.route('/<slug>', methods=['GET'])
def serve(slug=None):
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
    if _errors is not None:
        logging.warning('invalid json submission, redirecting to root page')
        return render_template('index.html', content='')

    slug = request.json.get('slug', None)
    url = request.json.get('url', None)

    if slug is not None and url is not None:
        logging.info('saving provided slug "{}" and url "{}" will then redirect to url'.format(slug, url))
        MappingCollection().save_mapping(slug, url)
        return redirect(url)

    elif url is not None and slug is None: # if providing a url, we need to create and store new slug
        slug = generate('1234567890abcdef', 5)  
        logging.info('saving NEW slug "{}" and url "{}" will then redirect to url'.format(slug, url))
        _errors = ''
        if not MappingCollection().save_mapping(slug, url):
            _errors = 'Failed to save'
            logging.warning('failed to save document {}'.format(_errors))
        return jsonify({'slug': slug, 'url':url,'errors':_errors})

    elif slug is not None and url is None:
        return serve(slug)


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

