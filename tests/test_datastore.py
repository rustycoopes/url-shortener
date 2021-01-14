
import pytest
from datastore import MappingCollection
from pymongo.errors import DuplicateKeyError

def test_will_save_and_return(mappingColl):
    mappingColl.save_mapping("slug", "aurl")
    mapping = mappingColl.load_mapping("slug")

    assert mapping["url"] == "aurl"

def test_will_error_if_slug_duplicate(mappingColl):
    with pytest.raises(DuplicateKeyError):
        mappingColl.save_mapping("slug", "aurl")
        mappingColl.save_mapping("slug", "aurl")

def test_will_error_if_slug_null(mappingColl):
    
    with pytest.raises(ValueError, match ="Slug must be non-null and non-empty"):
        mappingColl.save_mapping(None, "aurl")

def test_will_error_if_slug_empty(mappingColl):
    with pytest.raises(ValueError, match ="Slug must be non-null and non-empty"):
        mappingColl.save_mapping("", "aurl")