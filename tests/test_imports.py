def test_app_imports():
    from app.main import app

    assert app.title == "AitherBackend"
    assert app.version == "1.0.0"
