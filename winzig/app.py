from uuid import uuid4
import os

from sqlalchemy import create_engine
from flask import Flask, abort, request, session

from winzig.database import db_session
from winzig.cache import cache

env = 'WINZIG_SETTINGS'
app = Flask(__name__)
app.config.from_object('winzig.default_settings')

if os.environ.get(env):
    app.config.from_envvar(env)

import winzig.views  # noqa

engine = create_engine(app.config['DB_URI'], convert_unicode=True)
db_session.configure(bind=engine)
cache.configure(**app.config['REDIS_CONFIG'])


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    clean up before ending the http request.
    commit all changes and close the db connection
    """
    db_session.commit()
    db_session.remove()


@app.before_request
def csrf_protect():
    """
    if the request's method is POST, validate the csrf token. if fails, show
    403 error page
    """
    if request.method == "POST" and not app.config.get('TESTING'):
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    """
    use uuid4 to generate random string for csrf token
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid4().hex
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token
