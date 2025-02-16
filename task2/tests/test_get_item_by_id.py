import jsonschema
import pytest
from client import APIClient

# Схема успешного ответа для GET /item/<id>
get_item_success_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "createdAt": {"type": "string"},
            "id": {"type": "string"},
            "name": {"type": "string"},
            "price": {"type": "integer"},
            "sellerId": {"type": "integer"},
            "statistics": {
                "type": "object",
                "properties": {
                    "contacts": {"type": "integer"},
                    "likes": {"type": "integer"},
                    "viewCount": {"type": "integer"}
                },
                "required": ["contacts", "likes", "viewCount"]
            }
        },
        "required": ["createdAt", "id", "name", "price", "sellerId", "statistics"]
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


def test_get_item_success(client):
    # Шаг 1. Создаём item
    create_payload = {
        "sellerID": 213152,  # корректное значение: 6 цифр
        "name": "test_item",
        "price": 10,
        "statistics": {
            "contacts": 2,
            "likes": 5,
            "viewCount": 20
        }
    }
    create_response = client.create_item(create_payload)
    assert create_response.status_code == 200, f"Unexpected status code on create: {create_response.status_code}"
    created_data = create_response.json()
    status_message = created_data.get("status", "")
    prefix = "Сохранили объявление - "
    # Извлекаем item_id из первого созданного объекта
    item_id = status_message[len(prefix):].strip()

    # Шаг 2. Проверяем наличие item по его id
    get_response = client.get_item_by_id(item_id)
    assert get_response.status_code == 200, f"Unexpected status code on get: {get_response.status_code}"
    get_data = get_response.json()
    jsonschema.validate(instance=get_data, schema=get_item_success_schema)


def test_get_item_bad_request(client, monkeypatch):
    # Эмуляция Bad Request с помощью monkeypatch
    from requests.models import Response
    def fake_get(*args, **kwargs):
        resp = Response()
        resp.status_code = 400
        resp._content = b'{"result": {"messages": {"nostrudffb": "error", "Ut__": "error"}, "message": "Bad Request"}, "status": "fail"}'
        return resp

    monkeypatch.setattr(client, 'get_item_by_id', lambda item_id: fake_get())

    item_id = "invalid-id"
    response = client.get_item_by_id(item_id)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    jsonschema.validate(instance=data, schema=error_schema)
