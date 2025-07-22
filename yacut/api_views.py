from http import HTTPStatus

from flask import jsonify, request
from wtforms import ValidationError

from . import app
from .error_handlers import ImpossibleToCreate, InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_short_url(short_url):
    url_map = URLMap.get(short_url)
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True)
    if not data or not request.is_json:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса',
            HTTPStatus.BAD_REQUEST
        )
    original_link = data.get('url')
    print(original_link)
    custom_id = data.get('custom_id')
    if not original_link:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    try:
        url_map = URLMap.save(
            original_link,
            custom_id,
        )
        return jsonify(
            {
                'short_link': f'{request.host_url}{url_map.short}',
                'url': original_link
            }
        ), HTTPStatus.CREATED
    except (ValidationError, ImpossibleToCreate) as error:
        raise InvalidAPIUsage(str(error))
