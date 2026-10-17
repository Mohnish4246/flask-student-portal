import pytest

@pytest.fixture
def app(tmp_path,monkeypatch):
    # using seperate database for testing
    import database

    test_db = tmp_path / "test_students.db"

    monkeypatch.setattr(
        database,
        "DATABASE",
        str(test_db)
    )

    # import some settings from app.py
    from app import create_app

    app = create_app()

    app.config.update(
        TESTING = True,
        WTF_CSRF_ENABLED = False
    )

    yield app

@pytest.fixture
def client(app):
    return app.test_client()