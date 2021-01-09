
import webserver
import pytest



def test_send_only_url_will_create_slug( mocker, client):
    # TODO : FIX TEST
    url = "someUrl"
    mocker.patch('webserver.MappingCollection.save_mapping', return_value = True)
    payload = {"url":url}
    response = client.get("/", json=payload)
    result = response.get_json();
    
    
    assert result is not None
    assert "slug" in result
    assert result["url"] == url
    assert result["errors"] == ""
    pass

def test_send_only_url_will_respond_error_if_not_saved( mocker, client):
    # TODO : FIX TEST
    url = "someUrl"
    mocker.patch('webserver.MappingCollection.save_mapping', return_value = False)
    payload = {"url":url}
    response = client.get("/", json=payload)
    result = response.get_json();
    
    assert result is not None
    assert "slug" in result
    assert result["url"] == url
    assert result["errors"] == "Failed to save"
    pass

def test_send_url_and_slug_will_create_slug_and_redirect():
    # TODO : Implement test
    pass

def test_send_slug_only_redirects_if_exists():
    # TODO : Implement test
    pass

def test_send_slug_only_errors_if_not_exist():
    # TODO : Implement test
    pass

def test_send_no_slug_or_url_will_error():
    # TODO : Implement test
    pass

def test_send_slug_with_no_mapping_results_in_clear_message():
    # TODO : Implement test
    pass
