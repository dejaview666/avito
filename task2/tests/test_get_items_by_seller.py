import jsonschema
import pytest
from client import APIClient

# Схема успешного ответа для GET /<sellerId>/item (массив объектов объявления)
get_items_by_seller_success_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "sellerId": {"type": "integer"},
            "name": {"type": "string"},
            "price": {"type": "integer"},
            "statistics": {
                "type": "object",
                "properties": {
                    "likes": {"type": "integer"},
                    "viewCount": {"type": "integer"},
                    "contacts": {"type": "integer"}
                },
                "required": ["likes", "viewCount", "contacts"]
            },
            "createdAt": {"type": "string"}
        },
        "required": ["id", "sellerId", "name", "price", "statistics", "createdAt"]
    }
}

error_schema = {
    "type": "object",
    "properties": {
        "result": {
            "type": "object",
            "properties": {
                "messages": {"type": "object"},
                "message": {"type": "string"}
            },
            "required": ["messages", "message"]
        },
        "status": {"type": "string"}
    },
    "required": ["result", "status"]
}


@pytest.fixture
def client(base_url):
    return APIClient(base_url)


def test_get_items_by_seller_success(client):
    seller_id = 1234345231
    response = client.get_items_by_seller(seller_id)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=get_items_by_seller_success_schema)


def test_get_items_by_seller_bad_request(client, monkeypatch):
    # Эмуляция ответа Bad Request
    from requests.models import Response
    def fake_get(*args, **kwargs):
        resp = Response()
        resp.status_code = 400
        resp._content = b'{"result": {"messages": {"nostrudffb": "error", "Ut__": "error"}, "message": "Bad Request"}, "status": "fail"}'
        return resp

    monkeypatch.setattr(client, 'get_items_by_seller', lambda seller_id: fake_get())

    seller_id = "invalid"  # Передаём некорректное значение
    response = client.get_items_by_seller(seller_id)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=error_schema)


def test_get_items_by_seller_server_error(client, monkeypatch):
    from requests.models import Response
    def fake_get(*args, **kwargs):
        resp = Response()
        resp.status_code = 500
        resp._content = b'{"result": {"messages": {}, "message": "Internal Server Error"}, "status": "error"}'
        return resp

    monkeypatch.setattr(client, 'get_items_by_seller', lambda seller_id: fake_get())

    seller_id = 1234345231
    response = client.get_items_by_seller(seller_id)
    assert response.status_code == 500, f"Expected 500, got {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=error_schema)
