from sys import path
import os
#additionalPath = os.path.realpath('..\\')
#path.append(additionalPath)
#print(path)

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
    conf.read(r'.\config\test.cfg')
    dataStoreConnectionString = conf['datastore']['ConnectionString']
    collectionName = conf['datastore']['CollectionName']
    databaseName = conf['datastore']['DatabaseName']
    mappingColl = MappingCollection(dataStoreConnectionString, databaseName, collectionName)
    yield mappingColl
    mongoCollection = mappingColl._get_collecton()
    mongoCollection.remove({})

