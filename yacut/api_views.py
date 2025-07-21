from http import HTTPStatus

from flask import jsonify, request
from yacut import app, db

from .constants import ALLOWED_SYMBOLS, MAX_SHORT_URL_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import create_url_map


@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_short_url(short_url):
    url_map = URLMap.query.filter_by(short=short_url).first()
    if url_map:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
