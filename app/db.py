import sqlite3

import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


import csv


def read_geonames_file(file) -> list:
    reader = csv.reader(file, delimiter="\t")
    results = []
    for line in reader:
        results.append((line[1], line[4], line[5]))

    return results


def populate_db():
    db = get_db()

    with current_app.open_resource('data/cities5000.tsv', mode='r') as f:
        locations = read_geonames_file(f)

        for loc in locations:
            db.execute("INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)",
                       (loc[0], loc[1], loc[2])
                       )
        db.commit()


@click.command('pop-db')
@with_appcontext
def populate_db_command():
    """Populate the DB with test city data."""
    populate_db()
    click.echo('Populated the database')


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
