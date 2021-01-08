import pymongo


class MappingCollection:

    _client = None

    def save_mapping(self, slug, url):
        # TODO : consider unique index for collection to get error on insert 
        mappings = self._get_collecton()
        data = {'slug': slug, 'url':url}
        return mappings.insert_one(data).inserted_id is not None

    def load_mapping(self, slug):
        mappings = self._get_collecton()
        return mappings.find_one({'slug':slug})

    def _get_collecton(self):
        # TODO : Move connection string into configuration, possibly also database and collection name
        if self._client is None:
            self._client = pymongo.MongoClient('mongodb+srv://russ-admin:cooperman@cluster0.gqxah.mongodb.net/newDB?readPreference=secondary&retryWrites=true&w=majority')
        database = self._client.URLREDIRECT
        mappingCollection = database.SlugMapping
        return mappingCollection

    