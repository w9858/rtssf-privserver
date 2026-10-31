import pytest
from server import create_app

@pytest.fixture
def app(tmp_path):
    return create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'save.sqlite3'),
                       'ASSET_DIR': str(tmp_path / 'assets'), 'SPY_DURATION_SECONDS': 0})

@pytest.fixture
def client(app): return app.test_client()
