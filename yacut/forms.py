from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp
)

from .constants import (
    MAX_SHORT_URL_LENGTH,
    MAX_URL_LENGTH,
)


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, MAX_URL_LENGTH, message='Слишком длинная ссылка')
        ]
    )
    custom_id = StringField(
        'Короткая ссылка',
        validators=[
            Optional(),
            Length(
                1,
                MAX_SHORT_URL_LENGTH,
                message='Слишком длинный идентификатор'
            ),
            Regexp(r'^[a-zA-Z0-9]+$', message='Некорректный идентификатор')
        ]
    )
    submit = SubmitField('Создать')