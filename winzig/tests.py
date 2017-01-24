from flask_testing import TestCase
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy import create_engine

import winzig
from winzig.database import db_session, init_db

from urlzip.models import URLMap


class AppTestCase(TestCase):
    def setUp(self):
        engine = create_engine(winzig.app.config['DB_URI'],
                               convert_unicode=True)
        if not database_exists(engine.url):
            create_database(engine.url)
        db_session.configure(bind=engine)
        init_db()
        self.engine = engine
        self.db_session = db_session

    def tearDown(self):
        self.db_session.remove()
        drop_database(self.engine.url)

    def create_app(self):
        winzig.app.config['TESTING'] = True
        return winzig.app

    def test_homepage(self):
        self.client.get('/')
        self.assert_template_used('home.jinja2')
        self.assert_context("error", None)
        self.assert_context("url", None)

    def test_deflate_url_with_valid_url(self):
        with self.app.test_client() as client:
            client.get('/')
            self.client.post('/',
                             data={'url': 'google.com'},
                             follow_redirects=True)

            self.assert_template_used('home.jinja2')
            url = self.get_context_variable('url')
            self.assertIsNotNone(url)
            self.assertTrue(url.startswith('http://'))

    def test_deflate_url_with_invalid_url(self):
        with self.app.test_client() as client:
            client.get('/')
            self.client.post('/',
                             data={'url': 'google'},
                             follow_redirects=True)

            self.assert_template_used('home.jinja2')
            self.assertIsNone(self.get_context_variable('url'))
            self.assertIsNotNone(self.get_context_variable('error'))

    def test_inflate_url_redirects_to_404_page(self):
        self.db_session.add(URLMap(url='http://localhost/nuthing-jon-snu',
                                   id=1))
        self.db_session.flush()
        response = self.client.get('/jR', follow_redirects=True)
        self.assertEquals(404, response.status_code)
