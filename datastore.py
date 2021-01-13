import pymongo

class MappingCollection:

    _client = None
    def __init__(self, connectionString, databaseName, collectionName):
        self._connectionString = connectionString
        self._databaseName = databaseName
        self._collectionName = collectionName

    def save_mapping(self, slug, url):
        if slug is None or slug == "":
            raise ValueError("Slug must be non-null and non-empty")

        _mappings = self._get_collecton()
        _data = {'slug': slug, 'url':url}
        return _mappings.insert_one(_data).inserted_id is not None

    def load_mapping(self, slug):
        _mappings = self._get_collecton()
        return _mappings.find_one({'slug':slug})


    def load_all(self):
        _mappings = self._get_collecton()
        return _mappings.find()


    def _get_collecton(self):
        if self._client is None:
            self._client = pymongo.MongoClient(self._connectionString)
        _database = self._client[self._databaseName]
        _mappingCollection = _database[self._collectionName]
        return _mappingCollection

    