import pymongo


class MappingCollection:

    _client = None

    def save_mapping(self, slug, url):
        # TODO : consider unique index for collection to get error on insert 
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
        # TODO : Move connection string into configuration, possibly also database and collection name
        if self._client is None:
            self._client = pymongo.MongoClient('mongodb+srv://russ-admin:cooperman@cluster0.gqxah.mongodb.net/newDB?readPreference=secondary&retryWrites=true&w=majority')
        _database = self._client.URLREDIRECT
        _mappingCollection = _database.SlugMapping
        return _mappingCollection

    