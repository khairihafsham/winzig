from winzig.database import db_session
from urlzip.models import URLMap


def store_url(url):
    """For the given URL string, put into storage

    :url: url string
    :returns: URLMap
    """
    urlmap = URLMap(url=url)
    db_session.add(urlmap)
    db_session.flush()
    db_session.refresh(urlmap)

    return urlmap


def get_url_by_id(id):
    """Find the url_map row based on the id

    :id: integer of the row id
    :returns: URLMap object when found, None otherwise
    """
    return db_session.query(URLMap).get(id)


def get_url_by_url(url):
    """Find the url_map row by url column

    :url: url string
    :returns: URLMap if found, None otherwise
    """
    return db_session.query(URLMap).filter_by(url=url).first()
