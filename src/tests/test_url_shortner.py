import json

from app.api import views
from app.api.models import URL


def test_create_url(test_app, monkeypatch):
    test_request_payload = {"target_url": "https://google.com"}
    test_response_payload = {
        "target_url": "https://google.com",
        "is_active": True,
        "clicks": 1,
        "url": "http://localhost:8000/aminn",
        "admin_url": "http://localhost:8000/api/v1/admin/aminn_parvanian"
    }
    async def mock_create(url):
        return {
            "id":2,
            "target_url": "https://google.com",
            "is_active": True,
            "clicks": 1,
            "key": "aminn",
            "secret_key": "aminn_parvanian"
        }
    monkeypatch.setattr(URL(), "create", mock_create)

    def mock_info(db_url):
        return test_response_payload

    monkeypatch.setattr(views, "get_admin_info", mock_info)


    response = test_app.post("/api/v1/url", data=json.dumps(test_request_payload),)

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_create_url_invalid_json(test_app):
    test_request_payload = {"target_url": "googlecom"}
    test_response_payload = {
        "detail": "Your provided URL is not valid"
    }
    response = test_app.post("/api/v1/url", data=json.dumps(test_request_payload))
    assert response.status_code == 400
    assert response.json() == test_response_payload


def test_get_url(test_app, monkeypatch):
    
    class FakeURL:
        id = 2
        key = "aminn"
        secret_key = "aminn_parvanian"
        target_url = "https://google.com"
        is_active = True
        clicks = 1
        
        @staticmethod
        async def clicked():
            return None

    fake_url = FakeURL
        
    async def mock_get_by_key(url_key):
        return fake_url

    monkeypatch.setattr(URL, "get_by_key", mock_get_by_key)


    response = test_app.get("/api/v1/aminn", allow_redirects=False)
    assert response.status_code == 307


def test_get_incorrect_url(test_app, monkeypatch):
    
    async def mock_get_by_key(url_key):
        return None

    monkeypatch.setattr(URL, "get_by_key", mock_get_by_key)

    response = test_app.get("/api/v1/aminn")
    assert response.status_code == 404


def test_admin_url(test_app, monkeypatch):

    test_response_payload = {
        "target_url": "https://google.com",
        "is_active": True,
        "clicks": 1,
        "url": "http://localhost:8000/aminn",
        "admin_url": "http://localhost:8000/api/v1/admin/aminn_parvanian"
    }
    
    class FakeURL:
        id = 2
        key = "aminn"
        secret_key = "aminn_parvanian"
        target_url = "https://google.com"
        is_active = True
        clicks = 1
        
        @staticmethod
        async def clicked():
            return None

    fake_url = FakeURL
        
    async def mock_get_by_secret_key(secret_key):
        return fake_url

    monkeypatch.setattr(URL, "get_by_secret_key", mock_get_by_secret_key)

    def mock_info(url):
        return test_response_payload

    monkeypatch.setattr(views, "get_admin_info", mock_info)


    response = test_app.get("/api/v1/admin/aminn_parvanian")

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_admin_url_not_valid(test_app, monkeypatch):
    async def mock_get_by_secret_key(url_key):
        return None

    monkeypatch.setattr(URL, "get_by_secret_key", mock_get_by_secret_key)

    response = test_app.get("/notes/aminn_parvanian")
    assert response.status_code == 404


def test_deactive_admin_url(test_app, monkeypatch):

    class FakeURL:
        id = 2
        key = "aminn"
        secret_key = "aminn_parvanian"
        target_url = "https://google.com"
        is_active = True
        clicks = 1
        
        @staticmethod
        async def deactive():
            return None

    fake_url = FakeURL
        
    async def mock_get_by_secret_key(secret_key):
        return fake_url

    monkeypatch.setattr(URL, "get_by_secret_key", mock_get_by_secret_key)

    response = test_app.delete("/api/v1/admin/aminn_parvanian")

    assert response.status_code == 200
    assert response.json() == {"detail": f"Successfully deleted shortened URL for {fake_url.target_url}"}


def test_deactive_admin_url_not_valid(test_app, monkeypatch):
    async def mock_get_by_secret_key(url_key):
        return None
    
    monkeypatch.setattr(URL, "get_by_secret_key", mock_get_by_secret_key)
    
    response = test_app.get("/notes/aminn_parvanian")
    
    assert response.status_code == 404