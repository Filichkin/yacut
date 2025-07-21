from http import HTTPStatus
from flask import flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import create_url_map


@app.route('/', methods=['GET', 'POST'])
def index():
    """Функция для главной страницы."""

    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        short_url = form.custom_id.data

        if not original_link:
            flash('Введите оригинальную ссылку.')
            return render_template('main.html', form=form)

        if URLMap.query.filter_by(short=short_url).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('main.html', form=form)

        url_map = create_url_map(original_link, short_url)
        db.session.add(url_map)
        db.session.commit()
        return render_template(
            'main.html',
            form=form,
            short_url=url_map.short
        )
    return render_template('main.html', form=form)


@app.route('/<string:short_url>')
def redirect_to_original(short_url):
    """Функция для переадресации."""

    url_map = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(url_map.original), HTTPStatus.FOUND