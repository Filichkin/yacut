from datetime import datetime, timezone
import random
import re
import string

from wtforms.validators import ValidationError

from . import db
from .constants import (
    ALLOWED_SYMBOLS,
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
    def get(short, first_404=False):
        if first_404:
            return URLMap.query.filter_by(short=short).first_or_404()
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def save(original_link, short_url):
        if short_url:
            if len(short_url) > MAX_SHORT_URL_LENGTH:
                raise ValidationError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if not re.match(ALLOWED_SYMBOLS, short_url):
                raise ValidationError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if URLMap.get(short_url):
                raise ValueError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
        else:
            short_url = URLMap.get_unique_short_id()
        url_map = URLMap(original=original_link, short=short_url)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        return dict(
            original=self.original,
            short=self.short,
        )
