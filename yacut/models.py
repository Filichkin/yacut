from datetime import datetime, timezone

from . import db
from .constants import (
    MAX_SHORT_URL_LENGTH,
    MAX_URL_LENGTH,
)


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
    def get(short_url):
        return URLMap.query.filter_by(short=short_url).first()
