from datetime import datetime, timezone

from flask import url_for

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

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': url_for(
                'get_short_url',
                short_url=self.short,
                _external=True
            )
        }
