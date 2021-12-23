from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('locations', __name__)


@bp.route('/')
def index():
    db = get_db()
    locations = db.execute(
        'SELECT id, name, description, created, author_id'
        ' FROM locations '
        ' ORDER BY name DESC LIMIT 1000'
        ).fetchall()
    return render_template('locations/index.html', locations=locations)
