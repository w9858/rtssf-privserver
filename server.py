"""Application factory and the common wire/transaction boundary."""
import hmac
import importlib
import os
import sqlite3
import time
from pathlib import Path
import click
from flask import Flask, g, request, send_from_directory
from google.protobuf.message import DecodeError
from werkzeug.exceptions import HTTPException
from storage import Store

ROOT = Path(__file__).resolve().parent


def request_type(path):
    parts = path.strip('/').split('/')
    if len(parts) != 2: return None
    module, action = parts
    try:
        module = importlib.import_module(f'proto.{module}_pb2')
    except ModuleNotFoundError:
        return None
    name = 'Request' + ''.join(part.title() for part in action.split('_'))
    if path == '/unit/level_up': name = 'RequestLevelup'
    return getattr(module, name, None)


def create_app(config=None):
    from api import api
    app = Flask('Spyce', root_path=str(ROOT))
    app.config.from_mapping(
        DATABASE=os.environ.get('RTSSF_DATABASE', str(ROOT / 'instance' / 'save.sqlite3')),
        SEED_DIR=str(ROOT / 'data'),
        ASSET_DIR=os.environ.get('RTSSF_ASSET_DIR', str(ROOT / 'img')),
        API_TOKEN=os.environ.get('RTSSF_API_TOKEN', ''),
        MAX_CONTENT_LENGTH=1024 * 1024,
        SQLITE_VERSION='99',
        SPY_DURATION_SECONDS=3600,
        GAME_TIMEZONE=os.environ.get('RTSSF_GAME_TIMEZONE', 'Asia/Tokyo'),
    )
    if config: app.config.update(config)
    store = Store(app.config['DATABASE'], app.config['SEED_DIR'])
    app.extensions['store'] = store
    app.register_blueprint(api)
    api_namespaces = {name.rsplit('.', 1)[-1] for name in app.blueprints if name != 'api'}

    @app.before_request
    def begin():
        g.is_api = request.endpoint is not None and request.endpoint.startswith('api.')
        if not g.is_api:
            # Unknown routes in a game namespace must also carry a failure header.
            g.is_api = request.path.strip('/').split('/', 1)[0] in api_namespaces
            return
        token = app.config['API_TOKEN']
        if token and not hmac.compare_digest(request.headers.get('Authorization', '').encode('utf-8'), ('Bearer ' + token).encode('utf-8')):
            from werkzeug.exceptions import Unauthorized
            raise Unauthorized('A valid bearer token is required')
        cls = request_type(request.path)
        if cls is not None:
            message = cls()
            message.ParseFromString(request.get_data())
        g.db = store.connect()
        g.db.execute('BEGIN IMMEDIATE')

    @app.after_request
    def finish(response):
        connection = g.get('db')
        if connection is not None:
            if response.status_code < 400: connection.commit()
            else: connection.rollback()
        if g.get('is_api'):
            response.headers['Content-Type'] = 'application/x-protobuf'
            response.headers['X_SQLITE_VER'] = app.config['SQLITE_VERSION']
            response.headers['X_RES_STATUS'] = '0' if response.status_code < 400 else '1'
            response.headers['X_TIMESTAMP'] = str(int(time.time()))
            response.headers['Cache-Control'] = 'no-store'
        return response

    @app.teardown_request
    def close(error):
        connection = g.pop('db', None)
        if connection is not None:
            connection.rollback()
            connection.close()

    @app.errorhandler(DecodeError)
    def malformed(error):
        return api_error(400, 'Malformed protobuf request')

    @app.errorhandler(HTTPException)
    def http_error(error):
        if g.get('is_api'): return api_error(error.code, error.description)
        return error

    @app.errorhandler(sqlite3.OperationalError)
    def database_error(error):
        app.logger.exception('Database operation failed')
        return api_error(503, 'Save storage temporarily unavailable')

    @app.errorhandler(Exception)
    def unexpected(error):
        app.logger.exception('Request failed')
        return api_error(500, 'Internal server error')

    def api_error(status, message):
        # There is no shared Error message in the upstream protocol. Empty body
        # prevents HTML being mistaken for a valid game protobuf.
        response = app.make_response((b'', status))
        response.headers['X_ERROR_MSG'] = message.encode('ascii', 'replace').decode('ascii')[:200]
        return response

    @app.get('/healthz')
    def health():
        with store.transaction() as connection:
            connection.execute('SELECT 1').fetchone()
        return {'status': 'ok', 'mode': 'single-player', 'schema': 1}

    def assets(category, filename):
        return send_from_directory(str(Path(app.config['ASSET_DIR']) / category), filename)

    for category in ('assets', 'sqlites', 'images'):
        app.add_url_rule(f'/{category}/<path:filename>', category,
                         lambda filename, category=category: assets(category, filename))

    @app.cli.command('backup')
    @click.argument('destination', type=click.Path())
    def backup(destination):
        """Create a consistent online backup to a NEW destination file."""
        try: click.echo(str(store.backup(destination)))
        except ValueError as error: raise click.ClickException(str(error)) from error

    return app
