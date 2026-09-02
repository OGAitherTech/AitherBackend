def test_app_imports():
    from app.main import app

    assert app.title == "AitherBackend"
    assert app.version == "2.1.0"
