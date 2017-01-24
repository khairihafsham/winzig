import re

from hashids import Hashids
from formencode import validators, Invalid, All

from urlzip.storageservice import get_url_by_id, get_url_by_url, store_url
from urlzip.models import URLMap
from urlzip.exceptions import InvalidURL

scheme_re = re.compile('^https?://')


def deflate_url(url):
    """For the given URL string:
    1. run validation, if passes, then
    2. check if url exists, if yes return the hash string, otherwise
    3. create UrlMap and then return the hashid

    URL validation is done using the formencode validator for URL and also
    max string length of 2083, which is the limit for IE

    :url: url string
    :returns: hash string
    """
    url = add_http(url)

    try:
        validator = All(validators.URL(not_empty=True),
                        validators.String(max=2083))
        url = validator.to_python(url)
    except Invalid as err:
        raise InvalidURL(err.msg)

    urlmap = get_url_by_url(url)

    if not isinstance(urlmap, URLMap):
        urlmap = store_url(url)

    hashids = Hashids()

    return hashids.encode(urlmap.id)


def inflate_url(hash_str):
    """For the given hash_str, get the real id and find the record from
    storage. Returns the url if found, None otherwise

    :hash_str: string
    :returns: url string or None
    """
    hashids = Hashids()
    decoded = hashids.decode(hash_str)

    if len(decoded) > 0:
        urlmap = get_url_by_id(decoded[0])

        if isinstance(urlmap, URLMap):
            return urlmap.url

    return None


def add_http(url):
    """If http(s) is missing, add http

    :url: url string
    :returns: string that begins with http://
    """
    if scheme_re.search(url) is None:
        return 'http://%s' % url

    return url
