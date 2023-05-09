def test_ping(test_app):
    response = test_app.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == "Welcome to the URL shortener API :)"