from validation import validate_shortener_request
import pytest
from flask import Flask, request


app = Flask(__name__)

def test_is_valid_message(create_valid_mapping_request):
    json_input = create_valid_mapping_request(slug="Test")
    with app.test_request_context('/', json=json_input):
       errors = validate_shortener_request(request)
       assert errors is None
    json_input = create_valid_mapping_request(slug="Test")
    with app.test_request_context('/', json=json_input):
       errors = validate_shortener_request(request)
       assert errors is None


@pytest.mark.parametrize("required_parm_name", ["slug", "url"])
def test_is_valid_just_url(required_parm_name, create_valid_mapping_request):
    json_input = create_valid_mapping_request()
    del json_input[required_parm_name]
    with app.test_request_context('/', json=json_input):
       errors = validate_shortener_request(request)
       assert errors is None

def test_is_notvalid_neither_slug_or_url(create_invalid_mapping_request):
    json_input = create_invalid_mapping_request()
    with app.test_request_context('/', json=json_input):
       errors = validate_shortener_request(request)
       assert errors is not None
    