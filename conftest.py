from sys import path
import os
additionalPath = os.path.realpath('./tests/')
path.append(additionalPath)
print(path)

import webserver
import pytest
from configparser import ConfigParser
from datastore import MappingCollection


@pytest.fixture
def client():
    webserver.app.config['TESTING'] = True
    client = webserver.app.test_client()
    yield client

@pytest.fixture()
def mappingColl():
    conf = ConfigParser()  
    conf.read(r'./config/test.cfg')
    dataStoreConnectionString = conf['datastore']['ConnectionString']
    collectionName = conf['datastore']['CollectionName']
    databaseName = conf['datastore']['DatabaseName']
    mappingColl = MappingCollection(dataStoreConnectionString, databaseName, collectionName)
    yield mappingColl
    mongoCollection = mappingColl._get_collecton()
    mongoCollection.remove({})



@pytest.fixture()
def create_valid_mapping_request():
    """
    Helper function for creating a correctly-structured
    json request
    """
    def _create_valid_mapping_request(slug="fixture", url="fixURL"):
        return {
            "slug": slug,
            "url":url
        }
    return _create_valid_mapping_request

@pytest.fixture()
def create_invalid_mapping_request():
    """
    Helper function for creating a correctly-structured
    json request
    """
    def _create_invalid_mapping_request(name="fixture"):
        return {
            "name": name,
        }
    return _create_invalid_mapping_request