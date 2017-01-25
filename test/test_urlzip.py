from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from winzig.test_settings import DB_URI
from winzig.database import db_session, init_db, drop_db

from urlzip.urlservice import add_http, deflate_url, inflate_url
from urlzip.storageservice import store_url, get_url_by_id, get_url_by_url
from urlzip.models import URLMap
from urlzip.exceptions import InvalidURL


class URLServiceTestCase(TestCase):
    def test_add_http(self):
        items = (
            ('http://test', 'test'),
            ('http://test.com', 'test.com'),
            ('https://test.com', 'https://test.com')
        )

        for expected, param in items:
            self.assertEquals(expected, add_http(param))

    @patch('urlzip.urlservice.get_url_by_id')
    def test_inflate_url_gets_unknown_hash(self, mock_get_url_by_id):
        mock_get_url_by_id.return_value = None
        result = inflate_url('jR')
        self.assertIsNone(result)

    @patch('urlzip.urlservice.get_url_by_id')
    def test_inflate_url_gets_known_hash(self, mock_get_url_by_id):
        urlmap = URLMap(id=1, url="https://google.com")
        mock_get_url_by_id.return_value = urlmap
        result = inflate_url('jR')
        self.assertEquals('https://google.com', result)

    def test_deflate_url_raise_exception(self):
        with self.assertRaises(InvalidURL):
            deflate_url('noturl')

    @patch('urlzip.urlservice.get_url_by_url')
    @patch('urlzip.urlservice.store_url')
    def test_deflate_url_new_url(self, mock_store_url, mock_get_url_by_url):
        url = 'http://google.com'
        urlmap = URLMap(id=1, url=url)
        mock_get_url_by_url.return_value = None
        mock_store_url.return_value = urlmap
        result = deflate_url(url)

        self.assertEquals('jR', result)

    @patch('urlzip.urlservice.get_url_by_url')
    def test_deflate_url_known_url(self, mock_get_url_by_url):
        url = 'http://google.com'
        urlmap = URLMap(id=1, url=url)
        mock_get_url_by_url.return_value = urlmap
        result = deflate_url(url)

        self.assertEquals('jR', result)


class URLMapTestCase(TestCase):
    def test_urlmap_repr(self):
        urlmap = URLMap(id=1, url='http://google.com')
        self.assertEquals("<URLMap(id=1, url='http://google.com')>",
                          str(urlmap))


class BaseDbTestCase(TestCase):
    def setUp(self):
        engine = create_engine(DB_URI, convert_unicode=True)
        if not database_exists(engine.url):
            create_database(engine.url)
        db_session.configure(bind=engine)
        init_db()
        self.engine = engine
        self.db_session = db_session

    def tearDown(self):
        db_session.remove()
        drop_database(self.engine.url)


class DropDbTestCase(BaseDbTestCase):
    def test_drop_db(self):
        sql = "select count(*) from pg_catalog.pg_tables " \
              "where schemaname='public'"
        table_count = self.engine.execute(sql).scalar()
        self.assertGreater(table_count, 0)

        drop_db()

        table_count = self.engine.execute(sql).scalar()
        self.assertEquals(0, table_count)


class StorageServiceTestCase(BaseDbTestCase):
    def test_store_url(self):
        url = 'http://google.com'
        urlmap = store_url(url)
        self.assertIsInstance(urlmap, URLMap)
        self.assertEquals(urlmap.url, url)
        self.assertEquals(urlmap.id, 1)

    def test_get_url_by_id_no_record(self):
        self.assertIsNone(get_url_by_id(1))

    def test_get_url_by_id_has_record(self):
        url = 'http://google.com'
        urlmap = URLMap(url=url, id=1)
        self.db_session.add(urlmap)
        self.db_session.flush()

        result = get_url_by_id(1)
        self.assertIsInstance(result, URLMap)
        self.assertEquals(url, result.url)

    def test_get_url_by_url_no_record(self):
        self.assertIsNone(get_url_by_url('http://a.io'))

    def test_get_url_by_url_has_record(self):
        url = 'http://a.io'
        urlmap = URLMap(url=url)
        self.db_session.add(urlmap)
        self.db_session.flush()

        result = get_url_by_url(url)
        self.assertIsInstance(result, URLMap)
        self.assertEquals(url, result.url)
