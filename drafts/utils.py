import random
import string

from ..yacut.constants import DEFAULT_SHORT_URL_LENGTH
from ..yacut.models import URLMap


def generate_short_id():
    allowed_symbols = string.ascii_letters + string.digits
    return ''.join(random.choices(allowed_symbols, k=DEFAULT_SHORT_URL_LENGTH))


def get_unique_short_id():
    short_id = generate_short_id()
    if URLMap.query.filter_by(short=short_id).first():
        return get_unique_short_id()
    return short_id


def create_url_map(original_url, custom_id=None):
    url_map = URLMap()
    url_map.original = original_url
    url_map.short = custom_id if custom_id else get_unique_short_id()
    return url_map