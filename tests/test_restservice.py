
import webserver
import pytest



def test_send_only_url_will_create_slug( mocker, client):
    url = "someUrl"
    mocker.patch('webserver.MappingCollection.save_mapping', return_value = True)
    payload = {"url":url}
    response = client.get("/", json=payload)
    result = response.get_json();

    assert result is not None
    assert "slug" in result
    assert result["url"] == url
    assert result["errors"] == ""
    

def test_send_only_url_will_respond_error_if_not_saved( mocker, client):
    url = "someUrl"
    mocker.patch('webserver.MappingCollection.save_mapping', return_value = False)
    payload = {"url":url}
    response = client.get("/", json=payload)
    result = response.get_json();
    
    assert result is not None
    assert "slug" in result
    assert result["url"] == url
    assert result["errors"] == "Failed to save"

def test_send_url_and_slug_will_create_slug_and_redirect( mocker, client):
    url = "someUrl"
    slug = "someSlug"
    mocker.patch('webserver.MappingCollection.save_mapping', return_value = False)
    payload = {"url": url, "slug" : slug}
    redirect_function = mocker.patch('webserver.redirect', return_value = "myredirect")
    client.get("/", json=payload)
    webserver.redirect.assert_called_with(url)

    
def test_send_slug_only_redirects_if_exists( mocker, client):
    url = "someUrl"
    slug = "someSlug"
    payload = {"url": url, "slug" : slug}
    
    mocker.patch('webserver.MappingCollection.load_mapping', return_value = payload)
    redirect_function = mocker.patch('webserver.redirect', return_value = "myredirect")

    client.get("/{}".format(slug))
    webserver.redirect.assert_called_with(url)
    

def test_send_slug_only_errors_if_not_exist( client):
    slug = "doesntExist"
    response = client.get("/{}".format(slug))
    result = response.get_json();
    
    assert result is not None
    assert "error" in result
    assert result["error"] == "mapping not found, url to redirect could not be performed."

def test_send_no_slug_or_url_will_error(client):
    response = client.get("/")
    htmlPage = response.data.decode()
    assert "URL Shortener home" in htmlPage
    
    
