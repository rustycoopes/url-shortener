from sys import path
import os
#additionalPath = os.path.realpath('..\\')
#path.append(additionalPath)
#print(path)

import webserver
import pytest

@pytest.fixture
def client():
    webserver.app.config['TESTING'] = True
    client = webserver.app.test_client()
    yield client
