from http import HTTPStatus
import re

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


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True)
    if not data or not request.is_json:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса',
            HTTPStatus.BAD_REQUEST
        )
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > MAX_SHORT_URL_LENGTH:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST
            )
        if not re.match(ALLOWED_SYMBOLS, custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )

    url_map = create_url_map(data['url'], custom_id)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED