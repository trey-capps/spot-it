"""
To run this test in a module format use:
    python -m pytest tests/etl_tests/test_extract_load_mongo.py
in the SpotIt project directory
"""
from src.etl.etl_models.extract_load_mongo import ExtractLoadMongo
import etl.config as config

def test_mongo_connect_invalid_db_str():
    """Inaccurate mongo string"""
    cred = config.mongo_cred
    mongo_connect = ExtractLoadMongo(cred + 'a', "TempPosts", "CollectRaw")
    assert mongo_connect.mongo_connect() == None