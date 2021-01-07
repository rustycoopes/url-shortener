"""Basic hello message for flask app"""
import os
from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)


@app.route("/")
def view_mappings():
    return render_template("view.html", content="")

@app.route("/add")
def add():
   return render_template("add.html")

def is_development():
    return not "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")

if is_development():
    app.run(debug=True)

