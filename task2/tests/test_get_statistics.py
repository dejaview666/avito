import jsonschema
import pytest
from client import APIClient

# Схема успешного ответа для GET /statistic/<id> (массив объектов статистики)
statistics_success_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "likes": {"type": "integer"},
            "viewCount": {"type": "integer"},
            "contacts": {"type": "integer"}
        },
        "required": ["likes", "viewCount", "contacts"]
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


def test_get_statistics_success(client):
    item_id = "0cd4183f-a699-4486-83f8-b513dfde477a"
    response = client.get_statistics(item_id)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=statistics_success_schema)


def test_get_statistics_not_found(client, monkeypatch):
    from requests.models import Response
    def fake_get(*args, **kwargs):
        resp = Response()
        resp.status_code = 404
        resp._content = b'{"result": {"messages": {}, "message": "Not Found"}, "status": "fail"}'
        return resp

    monkeypatch.setattr(client, 'get_statistics', lambda item_id: fake_get())

    item_id = "non-existent-id"
    response = client.get_statistics(item_id)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=error_schema)


def test_get_statistics_server_error(client, monkeypatch):
    from requests.models import Response
    def fake_get(*args, **kwargs):
        resp = Response()
        resp.status_code = 500
        resp._content = b'{"result": {"messages": {}, "message": "Internal Server Error"}, "status": "error"}'
        return resp

    monkeypatch.setattr(client, 'get_statistics', lambda item_id: fake_get())

    item_id = "any-id"
    response = client.get_statistics(item_id)
    assert response.status_code == 500, f"Expected 500, got {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=error_schema)
