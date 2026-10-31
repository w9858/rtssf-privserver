"""Compatibility entry point: python app.py or gunicorn 'server:create_app()'."""
import os
from server import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host=os.environ.get('RTSSF_HOST', '127.0.0.1'),
            port=int(os.environ.get('RTSSF_PORT', '19212')), debug=False)
