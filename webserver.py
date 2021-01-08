"""Basic hello message for flask app"""
import os
from nanoid import generate
from flask import Flask, redirect, url_for, render_template, jsonify, request
app = Flask(__name__)
from invalid_usage import InvalidUsage
from validation import validate_shortener_request
from datastore import MappingCollection


@app.route("/mappings", methods=["GET"])
def view_mappings():
    # TODO : List mappings on screen
    return render_template("view.html", content="")

@app.route("/mapping/<slug>", methods=["GET"])
def view(slug):
    # TODO : Make this prettier, and provide adding functionatilty?
    mapping = MappingCollection().load_mapping(slug)
    return render_template("add.html", slug=mapping["slug"], url=mapping["url"])

@app.route("/<slug>", methods=["GET"])
def serve(slug=None):
    if slug is not None:
        mapping = MappingCollection().load_mapping(slug)
        if mapping is not None:
            return redirect(mapping["url"])
        else: 
            return jsonify({"error":"mapping not found, url to redirect could not be performed."})

@app.route("/", methods=["GET", "POST"])
def serve_or_save():
    
    errors = validate_shortener_request(request)
    if errors is not None:
       print(errors)
       raise InvalidUsage(errors)

    slug = request.json.get("slug", None)
    url = request.json.get("url", None)

    if slug is not None and url is not None:
        MappingCollection().save_mapping(slug, url)
        return redirect(url)

    elif url is not None and slug is None: # if providing a url, we need to create and store new slug
        slug = generate('1234567890abcdef', 5)  
        MappingCollection().save_mapping(slug, url)
        return jsonify({"slug": slug, "url":url})

    elif slug is not None and url is None:
        return serve(slug)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
   response = jsonify(error.to_dict())
   response.status_code = error.status_code
   return response

def is_development():
    return not "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")

if __name__ == '__main__':
    if is_development():
        app.run(debug=True)

