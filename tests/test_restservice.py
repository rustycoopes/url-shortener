
import webserver
import pytest


def test_send_only_url_will_create_slug( mocker, client):
    url = "someUrl"
    payload = {"url":url}
    response = client.get("/", json=payload)
    result = response.get_json();
    
    mocker.patch('webserver._save_mapping', return_value = True)
    
    assert result is not None
    assert "slug" in result
    assert result["url"] == url


def test_send_url_and_slug_will_create_slug_and_redirect():
    pass
def test_send_slug_only_redirects_if_exists():
    pass

def test_send_slug_only_errors_if_not_exist():
    pass

def test_send_no_slug_or_url_will_error():
    pass
