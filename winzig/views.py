from flask import (render_template, request, url_for, abort, redirect, flash,
                   get_flashed_messages)

from winzig.app import app

from urlzip.urlservice import inflate_url, deflate_url
from urlzip.exceptions import InvalidURL


@app.route('/', methods=['POST', 'GET'])
def deflate_url_view():
    """Deflate the URL submitted and return the shortened url.

    Implemented the POST/Redirect/GET technique to prevent double posting when
    user refreshes the page after submission.
    """
    hash_str = error = url = None

    if request.method == 'POST':
        try:
            hash_str = deflate_url(request.form.get('url', ''))
            flash(hash_str, 'hash_str')
        except InvalidURL as err:
            flash(str(err), 'error')

        return redirect(url_for('deflate_url_view'))

    if request.method == 'GET':
        messages = get_flashed_messages(category_filter=['hash_str'])
        hash_str = messages[0] if messages else None
        messages = get_flashed_messages(category_filter=['error'])
        error = messages[0] if messages else None

    if hash_str:
        url = url_for('inflate_url_view', hash_str=hash_str, _external=True)

    return render_template('home.jinja2', url=url, error=error)


@app.route('/<hash_str>', methods=['GET'])
def inflate_url_view(hash_str):
    """From the hash_str, redirect to original URL if found. Otherwise 404

    :hash_str: string
    """
    url = inflate_url(hash_str)

    if url is None:
        abort(404)

    return redirect(url)
