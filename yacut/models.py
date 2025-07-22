from datetime import datetime, timezone
import random
import string

from . import db
from .constants import (
    DEFAULT_SHORT_URL_LENGTH,
    MAX_GENARATE_ITERATIONS,
    MAX_SHORT_URL_LENGTH,
    MAX_URL_LENGTH,
)
from .error_handlers import ImpossibleToCreate


class URLMap(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String(MAX_URL_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(MAX_SHORT_URL_LENGTH),
        nullable=False,
        unique=True
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.now(timezone.utc)
    )

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_GENARATE_ITERATIONS):
            allowed_symbols = string.ascii_letters + string.digits
            short_id = ''.join(
                random.choices(allowed_symbols, k=DEFAULT_SHORT_URL_LENGTH)
            )
            if not URLMap.get(short_id):
                return short_id
        raise ImpossibleToCreate()

    @staticmethod
    def get(short_url):
        return URLMap.query.filter_by(short=short_url).first()
