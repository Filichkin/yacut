from http import HTTPStatus
from flask import flash, redirect, render_template

from . import app
from .error_handlers import ImpossibleToCreate
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    """Функция для главной страницы."""

    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        short_url = form.custom_id.data
        try:
            return render_template(
                'main.html',
                form=form,
                short_url=URLMap.save(original_link, short_url).short
            )
        except (ValueError, ImpossibleToCreate) as error:
            flash(str(error))
    return render_template('main.html', form=form)


@app.route('/<string:short_url>')
def redirect_to_original(short_url):
    """Функция для переадресации."""

    url_map = URLMap.get(short_url)
    return redirect(url_map.original), HTTPStatus.FOUND